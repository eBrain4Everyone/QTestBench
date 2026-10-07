"""
evaluate_solutions.py
=====================
Evaluates LLM‑generated pytest suites for the eight QHack challenges.

**Correctness (soundness + discrimination)** — Measured by **ES**, **CS**,
**BDS**, and **TQS = ES × CS × BDS** (when LLM probes are enabled).  **CS**
is the fraction of oracle‑*correct* solutions (human + labelled LLMs) that
pass all subtests; **BDS** is the fraction of oracle‑*wrong* LLM solutions
that are rejected.

**Coverage (input exercise)** — The primary coverage metric is
**coverage_inputs** (**C_in**): the fraction of *official* challenge inputs
that appear in the **LLM‑generated test body** after removing the
framework‑injected ``TEST_CASES`` block.  If the body contains a loop
``for ... in TEST_CASES``, **C_in = 1.0** (all official pairs are
reachable).  A legacy **coverage_literal** value (match on the full file)
is kept for diagnostics; it is often inflated toward 1.0 because the
injected list contains every input string.

**Composite research score** — **CQ = sqrt(TQS × C_in)** balances
discriminative quality with exercised official cases (geometric mean in
[0, 1]).

See also: ``--human-only`` for human‑baseline runs; reports include
``pytest_output`` excerpts on failures.
"""

import os
import sys
import json
import re
import ast
import math
import subprocess
import tempfile
import argparse
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from config import (
    FRAMEWORK_ROOT,
    GENERATED_TESTS_SUBDIR,
    CHALLENGE_NAMES,
    LLM_SOLUTION_MODELS,
    LLM_SOLUTION_VARIANTS,
    DEFAULT_MODEL,
    MODELS,
)
from challenge_mapper import (
    ChallengeMapper, ChallengeInfo, HumanSolution, LLMSolution
)
from notebook_utils import inject_harness_if_missing

# Test types produced by the generator
TEST_TYPES = ["syntactic", "semantic", "behavioral"]


# ---------------------------------------------------------------------------
# CORRECTNESS ORACLE
# ---------------------------------------------------------------------------
# The oracle harness remains unchanged: it runs a solution on the official
# test cases and reports how many pass, fail or error.  This is used to
# label LLM solutions as CORRECT or WRONG when human_only is False.

_ORACLE_HARNESS = '''
import sys
import json
import warnings
warnings.filterwarnings("ignore")

try:
    import pennylane as qml
    import pennylane.numpy as np
except ImportError:
    qml = None
    import numpy as np

SOLUTION_CODE = {solution_code!r}
TEST_CASES    = {test_cases!r}

ns = {{
    "json": json, "qml": qml, "np": np,
    "__name__": "__oracle__", "__builtins__": __builtins__,
}}

try:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        exec(compile(SOLUTION_CODE, "<solution>", "exec"), ns)
except SystemExit:
    pass
except Exception as e:
    print("LOAD_ERROR:" + str(e)[:200])
    sys.exit(2)

run_fn   = ns.get("run")
check_fn = ns.get("check")

if run_fn is None:
    print("MISSING_RUN"); sys.exit(2)
if check_fn is None:
    print("MISSING_CHECK"); sys.exit(2)

passed = failed = errors = 0
for inp, expected in TEST_CASES:
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            output = run_fn(inp)
        check_fn(output, expected)
        passed += 1
    except SystemExit:
        passed += 1
    except AssertionError:
        failed += 1
    except Exception:
        errors += 1

print("PASSED:" + str(passed))
print("FAILED:" + str(failed))
print("ERRORS:" + str(errors))
sys.exit(0 if (failed == 0 and errors == 0) else 1)
'''


def determine_correctness(
    solution_code: str,
    test_cases:    List[Tuple[str, str]],
    challenge_name: str,
) -> Tuple[Optional[bool], str]:
    """
    Returns (is_correct, detail).
      True  = all official test_cases pass
      False = at least one fails
      None  = could not determine
    """
    if not test_cases:
        return None, "no_test_cases"

    harness = _ORACLE_HARNESS.format(
        solution_code=solution_code,
        test_cases=test_cases,
    )

    with tempfile.TemporaryDirectory(prefix="qhack_oracle_") as tmpdir:
        tmp = Path(tmpdir)
        (tmp / "oracle.py").write_text(harness, encoding="utf-8")
        try:
            proc = subprocess.run(
                [sys.executable, str(tmp / "oracle.py")],
                capture_output=True, text=True,
                timeout=90, cwd=str(tmp),
            )
            out = proc.stdout + proc.stderr
        except subprocess.TimeoutExpired:
            return None, "oracle_timeout"
        except Exception as e:
            return None, "oracle_error: " + str(e)[:80]

    if "LOAD_ERROR"    in out: return None, "load_error: " + out[out.find("LOAD_ERROR:")+11:][:80]
    if "MISSING_RUN"   in out: return None, "missing_harness"
    if "MISSING_CHECK" in out: return None, "missing_harness"

    p = int(re.search(r"PASSED:(\d+)", out).group(1)) if re.search(r"PASSED:(\d+)", out) else 0
    f = int(re.search(r"FAILED:(\d+)", out).group(1)) if re.search(r"FAILED:(\d+)", out) else 0
    e = int(re.search(r"ERRORS:(\d+)", out).group(1)) if re.search(r"ERRORS:(\d+)", out) else 0

    n = len(test_cases)
    is_correct = (f == 0 and e == 0 and p == n and p > 0)
    detail = "passed {}/{}".format(p, n)
    if f: detail += ", {} failed".format(f)
    if e: detail += ", {} errors".format(e)
    return is_correct, detail


# ---------------------------------------------------------------------------
# DATA CLASSES
# ---------------------------------------------------------------------------

@dataclass
class SolutionLabel:
    solution_id:   str
    is_correct:    Optional[bool]
    oracle_detail: str = ""


@dataclass
class SingleRunResult:
    """Result of running one test file against one solution."""
    solution_id:      str
    solution_correct: Optional[bool]   # True / False / None
    executable:       bool  = False
    passed:           int   = 0
    failed:           int   = 0
    errors:           int   = 0
    total:            int   = 0
    error_label:      str   = ""
    error_detail:     str   = ""
    pytest_output:    str   = ""  # tail of pytest stdout/stderr when useful


@dataclass
class TestFileQuality:
    """
    Quality scores for one generated test file
    (test_syntactic.py / test_semantic.py / test_behavioral.py).
    Records ES / CS / BDS / TQS, injection-aware **coverage_inputs** (C_in),
    **cq** = sqrt(TQS × C_in), and **diversity** (breadth of ``test_*`` × C_in).
    """
    challenge:      str
    test_gen_model: str
    test_type:      str          # syntactic | semantic | behavioral

    # --- Raw execution results ---
    human_run:    Optional[SingleRunResult] = None
    llm_runs:     List[SingleRunResult]     = field(default_factory=list)

    # --- The three core scores [0, 1] ---
    es:  float = 0.0    # Executability Score
    cs:  float = 0.0    # Correctness Score   (accepts correct solutions)
    bds: float = 0.0    # Bug‑Detection Score (catches wrong solutions)
    tqs: float = 0.0    # Overall Test Quality Score = ES × CS × BDS

    # --- Supporting counts ---
    n_correct_total: int = 0   # human + correct LLMs tested
    n_correct_pass:  int = 0   # of those, how many passed
    n_wrong_total:   int = 0   # wrong LLMs tested
    n_wrong_fail:    int = 0   # of those, how many failed (correctly rejected)
    n_unknown:       int = 0   # solutions with unknown correctness

    # --- Coverage & diversity (paper-style) ---
    # coverage_inputs (C_in): official inputs exercised in LLM body (see module doc)
    coverage_inputs: float = 0.0
    coverage_literal: float = 0.0   # full file literal match (often inflated)
    uses_test_cases_loop: bool = False
    n_assertions: int = 0
    diversity: float = 0.0   # sqrt(C_in * breadth of test_* fns)
    cq: float = 0.0          # sqrt(TQS * coverage_inputs) — composite research score

    # --- Error info ---
    error_label:  str = ""
    error_detail: str = ""


@dataclass
class ChallengeQuality:
    """Aggregated quality scores for all 3 test files of one challenge."""
    challenge:           str
    test_gen_model:      str
    human_solution_used: str = ""

    # Per‑type test files
    test_files: List[TestFileQuality] = field(default_factory=list)

    # Solution correctness breakdown
    n_llm_solutions:       int = 0
    n_correct_solutions:   int = 0
    n_wrong_solutions:     int = 0
    n_unknown_solutions:   int = 0

    # Aggregated scores across all 3 test files
    avg_es:  float = 0.0
    avg_cs:  float = 0.0
    avg_bds: float = 0.0
    avg_tqs: float = 0.0
    avg_coverage_inputs: float = 0.0   # average C_in across test types
    avg_cov_literal: float = 0.0       # diagnostic: literal match on full file
    avg_cq: float = 0.0                # average composite CQ
    avg_div: float = 0.0

    # When --eval-all-human: every human solution in the pool
    human_evaluations_all: List[Dict[str, Any]] = field(default_factory=list)

    # Per‑type scores
    scores_by_type: Dict[str, Dict[str, float]] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# PYTEST RUNNER
# ---------------------------------------------------------------------------

def run_test_against_solution(
    test_file:        Path,
    solution_code:    str,
    solution_id:      str,
    solution_correct: Optional[bool],
    challenge_name:   str,
    template_path:    Optional[Path] = None,
) -> SingleRunResult:
    """Run one generated test file against one solution. Return results."""

    if template_path is not None:
        solution_code = inject_harness_if_missing(solution_code, template_path)

    result = SingleRunResult(
        solution_id=solution_id,
        solution_correct=solution_correct,
    )

    if not test_file.exists():
        result.error_label  = "SYNTAX_ERROR"
        result.error_detail = "Test file does not exist"
        return result

    try:
        ast.parse(test_file.read_text(encoding="utf-8", errors="replace"))
    except SyntaxError as e:
        result.error_label  = "SYNTAX_ERROR"
        result.error_detail = "line {}: {}".format(e.lineno, e.msg)
        return result

    test_src = test_file.read_text(encoding="utf-8", errors="replace")

    with tempfile.TemporaryDirectory(prefix="qhack_eval_") as tmpdir:
        tmp = Path(tmpdir)
        (tmp / "solution_module.py").write_text(solution_code, encoding="utf-8")
        (tmp / test_file.name).write_text(test_src, encoding="utf-8")

        conftest = (
            "import builtins as _b, sys, warnings\n"
            "warnings.filterwarnings('ignore')\n"
            "from pathlib import Path\n"
            "sys.path.insert(0, str(Path(__file__).parent))\n"
            "_b.INJECTED_SOLUTION_CODE = open(\n"
            "    Path(__file__).parent / 'solution_module.py',\n"
            "    encoding='utf-8').read()\n"
            "_b.INJECTED_CHALLENGE_NAME = {!r}\n".format(challenge_name)
        )
        (tmp / "conftest.py").write_text(conftest, encoding="utf-8")

        try:
            proc = subprocess.run(
                [sys.executable, "-m", "pytest",
                 str(tmp / test_file.name),
                 "-v", "--tb=short", "--no-header", "-q",
                 "--timeout=60", "-p", "no:warnings"],
                capture_output=True, text=True,
                timeout=180, cwd=str(tmp),
            )
            output = proc.stdout + proc.stderr
        except subprocess.TimeoutExpired:
            result.error_label  = "TIMEOUT"
            result.error_detail = "Whole-file timeout (180 s)"
            result.pytest_output = ""
            return result
        except Exception as e:
            result.error_label  = "RUNTIME_ERROR"
            result.error_detail = str(e)[:200]
            result.pytest_output = ""
            return result

    passed, failed, errors = _parse_counts(output)
    total = passed + failed + errors

    result.executable  = True
    result.passed      = passed
    result.failed      = failed
    result.errors      = errors
    result.total       = total

    if errors > 0 or total == 0:
        result.error_label  = _classify_error(output)
        result.error_detail = _extract_error_detail(output)
        if result.error_label in ("IMPORT_ERROR", "RUNTIME_ERROR", "SYNTAX_ERROR"):
            result.executable = False

    if failed > 0 or errors > 0 or not result.executable:
        result.pytest_output = _pytest_tail(output, max_chars=5000)
    return result


def _parse_counts(output: str) -> Tuple[int, int, int]:
    passed = failed = errors = 0
    m = re.search(r"(\d+) passed", output);  passed = int(m.group(1)) if m else 0
    m = re.search(r"(\d+) failed", output);  failed = int(m.group(1)) if m else 0
    m = re.search(r"(\d+) error",  output);  errors = int(m.group(1)) if m else 0
    if passed + failed + errors == 0:
        passed = output.count(" PASSED")
        failed = output.count(" FAILED")
        errors = output.count(" ERROR")
    return passed, failed, errors


def _classify_error(output: str) -> str:
    out = output.lower()
    if "syntaxerror"    in out: return "SYNTAX_ERROR"
    if "importerror"    in out: return "IMPORT_ERROR"
    if "modulenotfound" in out: return "IMPORT_ERROR"
    if "assertionerror" in out: return "ASSERTION_ERROR"
    if "timeout"        in out: return "TIMEOUT"
    return "RUNTIME_ERROR"


def _extract_error_detail(output: str) -> str:
    for line in output.splitlines():
        s = line.strip()
        if any(t in s for t in ("Error", "FAILED", "assert")) and len(s) > 10:
            return s[:200]
    return ""


def _pytest_tail(output: str, max_chars: int = 5000) -> str:
    """Keep the end of pytest output (assertions and tracebacks appear there)."""
    text = output.strip()
    if len(text) <= max_chars:
        return text
    return "...[truncated]\n" + text[-max_chars:]


# ---------------------------------------------------------------------------
# COVERAGE CALCULATION
# ---------------------------------------------------------------------------

def strip_injected_test_cases_block(src: str) -> str:
    """
    Remove the framework-prepended ``# --- Official test cases`` … ``TEST_CASES = [...]``
    block so metrics reflect only LLM-written lines
    (see ``generate_tests.official_test_cases_block``).
    If no injected marker is found, returns ``src`` unchanged.
    """
    idx = src.find("# --- Official test cases")
    if idx < 0:
        return src
    sub = src[idx:]
    m = re.search(r"^\s*TEST_CASES\s*=\s*\[", sub, re.M)
    if not m:
        return src
    bracket = idx + m.end() - 1
    depth = 0
    for i, ch in enumerate(src[bracket:], start=bracket):
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                rest = src[i + 1 :].lstrip("\n")
                head = src[:idx].rstrip()
                if head:
                    return head + "\n\n" + rest
                return rest
    return src


_TC_LOOP_RE = re.compile(
    r"for\s+[\w\s,()]+\s+in\s+TEST_CASES\b",
    re.MULTILINE,
)


def uses_official_test_cases_loop(body: str) -> bool:
    """True if generated tests iterate the injected ``TEST_CASES`` list."""
    return bool(_TC_LOOP_RE.search(body))


def count_pytest_assertions(body: str) -> int:
    """Approximate count of ``assert`` statements in test body (auditability)."""
    try:
        tree = ast.parse(body)
    except SyntaxError:
        return body.count(" assert ")
    n = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Assert):
            n += 1
    return n


def compute_coverage_literal(test_src: str, test_cases: List[Tuple[str, str]]) -> float:
    """
    Fraction of official inputs whose string appears somewhere in ``test_src``.
    On the full generated file this is often ~1.0 because ``TEST_CASES`` is injected.
    """
    total = len(test_cases)
    if total == 0:
        return 0.0
    used = set()
    for inp, _ in test_cases:
        literal = repr(inp)
        if literal in test_src or inp in test_src or '"{}"'.format(inp) in test_src:
            used.add(inp)
    return len(used) / total


def compute_coverage_inputs(
    full_src: str,
    test_cases: List[Tuple[str, str]],
) -> Tuple[float, float, bool, int]:
    """
    Primary coverage **C_in**: input-exercise rate on LLM body only.

    Returns (coverage_inputs, coverage_literal_full, uses_loop, n_assertions).
    If ``for ... in TEST_CASES`` appears in the stripped body, C_in = 1.0
    (all official pairs are exercised by construction).
    """
    lit = compute_coverage_literal(full_src, test_cases)
    body = strip_injected_test_cases_block(full_src)
    n_asr = count_pytest_assertions(body)
    if not test_cases:
        return 0.0, lit, False, n_asr
    if uses_official_test_cases_loop(body):
        return 1.0, lit, True, n_asr
    cin = compute_coverage_literal(body, test_cases)
    return cin, lit, False, n_asr


def compute_diversity(
    body_for_metrics: str,
    coverage_inputs: float,
) -> float:
    """
    Geometric mean of **C_in** and breadth (``test_*`` count / 3).
    ``body_for_metrics`` should be the stripped LLM body when available.
    """
    n_tests = len(re.findall(r"^def test_", body_for_metrics, re.M))
    breadth = min(1.0, n_tests / 3.0) if n_tests else 0.0
    return round(
        min(1.0, math.sqrt(max(coverage_inputs, 1e-9) * max(breadth, 1e-9))),
        4,
    )


def compute_composite_cq(tqs: float, coverage_inputs: float) -> float:
    """CQ = sqrt(TQS * C_in); balances discrimination and input exercise."""
    return round(
        min(1.0, math.sqrt(max(tqs, 0.0) * max(coverage_inputs, 1e-9))),
        4,
    )


# ---------------------------------------------------------------------------
# SCORE COMPUTATION
# ---------------------------------------------------------------------------

def _is_full_pass(r: SingleRunResult) -> bool:
    """True if the test ran and ALL sub-tests passed."""
    return r.executable and r.passed > 0 and r.failed == 0 and r.errors == 0


def _is_full_fail(r: SingleRunResult) -> bool:
    """True if the test ran but at least one sub-test failed (correctly rejected)."""
    return r.executable and (r.failed > 0 or r.errors > 0)


def compute_scores(tfq: TestFileQuality, human_only: bool = False) -> TestFileQuality:
    """
    Compute ES, CS, BDS, TQS for a TestFileQuality object.

    ES  — Executability Score
          1.0 if the test ran without crashing on the human solution
          0.0 otherwise

    CS  — Correctness Score
          Fraction of CORRECT solutions (human + correct LLMs) that the
          test passes.  A perfect test accepts ALL correct solutions → CS = 1.0
          Computed only over executable runs.  In human_only mode this
          reduces to whether the human passed.

    BDS — Bug‑Detection Score
          Fraction of WRONG solutions that the test correctly fails.
          A perfect test rejects ALL wrong solutions → BDS = 1.0
          Computed only over executable runs.  In human_only mode there are
          no wrong solutions so BDS remains 0.

    TQS — Test Quality Score
          ES × CS × BDS
          A single number in [0, 1] that is high only when all three
          properties hold simultaneously.
    """
    hr = tfq.human_run

    # ── ES ────────────────────────────────────────────────────────────────
    if hr is None or not hr.executable:
        tfq.es = 0.0
        tfq.cs = 0.0
        tfq.bds = 0.0
        tfq.tqs = 0.0
        return tfq

    tfq.es = 1.0

    # ── CS ────────────────────────────────────────────────────────────────
    # Correct pool = human solution + LLM solutions labelled CORRECT
    correct_runs: List[SingleRunResult] = []

    # Human solution counts as one correct run
    correct_runs.append(hr)

    if not human_only:
        # Correct LLM solutions
        for r in tfq.llm_runs:
            if r.solution_correct is True and r.executable:
                correct_runs.append(r)

    tfq.n_correct_total = len(correct_runs)
    tfq.n_correct_pass  = sum(1 for r in correct_runs if _is_full_pass(r))

    tfq.cs = (tfq.n_correct_pass / tfq.n_correct_total
              if tfq.n_correct_total > 0 else 0.0)

    # ── BDS ───────────────────────────────────────────────────────────────
    if human_only:
        tfq.bds = 0.0
        # Without wrong-solution probes, BDS is undefined; use ES*CS as the
        # composite "human validation" score (else TQS would always be 0).
        tfq.tqs = tfq.es * tfq.cs
        return tfq

    wrong_runs = [r for r in tfq.llm_runs
                  if r.solution_correct is False and r.executable]

    tfq.n_wrong_total = len(wrong_runs)
    tfq.n_wrong_fail  = sum(1 for r in wrong_runs if _is_full_fail(r))
    tfq.n_unknown     = sum(1 for r in tfq.llm_runs if r.solution_correct is None)

    tfq.bds = (tfq.n_wrong_fail / tfq.n_wrong_total
               if tfq.n_wrong_total > 0 else 0.0)

    # ── TQS ───────────────────────────────────────────────────────────────
    tfq.tqs = tfq.es * tfq.cs * tfq.bds

    return tfq


# ---------------------------------------------------------------------------
# HUMAN SOLUTION PICKER
# ---------------------------------------------------------------------------

def pick_best_human_solution(
    solutions:           List[HumanSolution],
    test_dir:            Path,
    challenge_name:      str,
    template_path:       Optional[Path] = None,
    prefer_solution_set: Optional[str] = None,
) -> Optional[HumanSolution]:
    """
    Run all available human solutions against the generated tests and pick
    the one that passes the most sub-tests.  Falls back to first ``.py`` file
    in the preferred set (or overall) if no tests exist yet.

    If ``prefer_solution_set`` is set (e.g. ``\"Solution3\"``) and at least one
    solution lives in that folder, only those candidates are considered.
    """
    if not solutions:
        return None

    pool = solutions
    if prefer_solution_set:
        pref = [s for s in solutions if s.solution_set == prefer_solution_set]
        if pref:
            pool = pref

    test_files = list(test_dir.glob("test_*.py")) if test_dir.exists() else []
    if not test_files:
        py = [s for s in pool if s.path.suffix == ".py"]
        return py[0] if py else pool[0]

    best, best_score = None, -1
    for sol in pool:
        score = 0
        for tf in test_files[:3]:
            r = run_test_against_solution(
                tf, sol.code,
                "{}/{}".format(sol.solution_set, sol.path.name),
                True, challenge_name,
                template_path=template_path,
            )
            score += r.passed
        if score > best_score:
            best_score = score
            best = sol
    return best


# ---------------------------------------------------------------------------
# CORE EVALUATOR
# ---------------------------------------------------------------------------

class TestQualityEvaluator:

    def __init__(
        self,
        framework_root: Path,
        test_gen_model: str = DEFAULT_MODEL,
        llm_models:     Optional[List[str]] = None,
        variants:       Optional[List[str]] = None,
        only:           Optional[List[str]] = None,
        human_only:     bool = False,
        prefer_human_set: Optional[str] = None,
        eval_all_human:   bool = False,
    ):
        self.framework_root = Path(framework_root)
        self.test_gen_model = test_gen_model
        self.tests_root     = self.framework_root / GENERATED_TESTS_SUBDIR
        self.llm_models     = llm_models or LLM_SOLUTION_MODELS
        self.variants       = variants   or LLM_SOLUTION_VARIANTS
        self.only           = only
        self.human_only     = human_only
        self.prefer_human_set = prefer_human_set
        self.eval_all_human   = eval_all_human

    # ── PUBLIC ENTRY POINT ────────────────────────────────────────────────

    def run(self) -> List[ChallengeQuality]:
        mapper = ChallengeMapper(str(self.framework_root))

        print("\n[1] Loading challenge data ...")
        ch_map = mapper.load_challenges()

        print("\n[2] Loading human solutions ...")
        human_map = mapper.load_human_solutions()

        # In human_only mode we skip loading LLM solutions entirely
        if not self.human_only:
            print("\n[3] Loading LLM solutions ...")
            llm_map = mapper.load_llm_solutions(
                llm_models=self.llm_models,
                variants=self.variants,
            )
        else:
            llm_map = defaultdict(lambda: defaultdict(list))

        challenges = list(ch_map.values())
        if self.only:
            challenges = [c for c in challenges if c.name in self.only]

        # Label LLM solutions via oracle if not human_only
        labels: Dict[str, Dict[str, SolutionLabel]] = {}
        if not self.human_only:
            print("\n[4] Labelling LLM solution correctness via oracle ...")
            for ch in challenges:
                labels[ch.name] = {}
                all_sols = [s for m in self.llm_models
                            for s in llm_map[ch.name].get(m, [])]
                for sol in all_sols:
                    sid = "{}/{}".format(sol.llm_model, sol.variant)
                    is_correct, detail = determine_correctness(
                        sol.code, ch.test_cases, ch.name)
                    labels[ch.name][sid] = SolutionLabel(sid, is_correct, detail)
                    status = ("CORRECT" if is_correct is True
                              else "WRONG"   if is_correct is False
                              else "UNKNOWN")
                    inj = " [harness-injected]" if sol.harness_injected else ""
                    print("    {} | {} -> {}{}  ({})".format(
                        ch.name, sid, status, inj, detail))
        else:
            # provide empty labels when no LLM solutions are present
            for ch in challenges:
                labels[ch.name] = {}

        print("\n[{}] Evaluating test quality ...".format(5 if not self.human_only else 3))
        results = []
        for ch in challenges:
            cq = self._evaluate_challenge(ch, human_map, llm_map, labels[ch.name])
            results.append(cq)

        return results

    # ── PER-CHALLENGE ─────────────────────────────────────────────────────

    def _evaluate_challenge(
        self,
        challenge:  ChallengeInfo,
        human_map:  Dict,
        llm_map:    Dict,
        labels:     Dict[str, SolutionLabel],
    ) -> ChallengeQuality:

        print("\n" + "-" * 65)
        print("  Challenge : {}".format(challenge.name))
        print("-" * 65)

        cq = ChallengeQuality(
            challenge=challenge.name,
            test_gen_model=self.test_gen_model,
        )

        test_dir = self.tests_root / challenge.name / self.test_gen_model

        # Pick best human solution (optionally restricted to e.g. Solution3/)
        all_human  = human_map.get(challenge.name, [])
        human_sol  = pick_best_human_solution(
            all_human, test_dir, challenge.name,
            template_path=challenge.template_path,
            prefer_solution_set=self.prefer_human_set,
        )
        if human_sol is None:
            print("  WARNING: No human solution found -- skipping")
            return cq

        cq.human_solution_used = "{}/{}".format(
            human_sol.solution_set, human_sol.path.name)

        # Collect all LLM solutions if not human_only
        if not self.human_only:
            all_llm = [s for m in self.llm_models
                       for s in llm_map[challenge.name].get(m, [])]
        else:
            all_llm = []

        cq.n_llm_solutions     = len(all_llm)
        cq.n_correct_solutions = sum(
            1 for sol in all_llm
            if labels.get("{}/{}".format(sol.llm_model, sol.variant),
                          SolutionLabel("", None)).is_correct is True)
        cq.n_wrong_solutions   = sum(
            1 for sol in all_llm
            if labels.get("{}/{}".format(sol.llm_model, sol.variant),
                          SolutionLabel("", None)).is_correct is False)
        cq.n_unknown_solutions = (cq.n_llm_solutions
                                   - cq.n_correct_solutions
                                   - cq.n_wrong_solutions)

        print("  Human baseline : {} (best of {})".format(
            cq.human_solution_used, len(all_human)))
        if not self.human_only:
            print("  LLM solutions  : {} total | {} correct | {} wrong | {} unknown".format(
                cq.n_llm_solutions, cq.n_correct_solutions,
                cq.n_wrong_solutions, cq.n_unknown_solutions))

        # Evaluate each test type
        for test_type in TEST_TYPES:
            test_file = test_dir / "test_{}.py".format(test_type)
            print("\n  [{}]".format(test_type.upper()))

            tfq = self._evaluate_one_test_file(
                test_file, test_type, challenge,
                human_sol, all_llm, labels)
            cq.test_files.append(tfq)

        human_pool = all_human
        if self.prefer_human_set:
            pref = [s for s in all_human if s.solution_set == self.prefer_human_set]
            if pref:
                human_pool = pref

        if self.eval_all_human:
            print("\n  [--eval-all-human] Per-solution human runs ...")
            for sol in human_pool:
                sid = "{}/{}".format(sol.solution_set, sol.path.name)
                entry: Dict[str, Any] = {"solution_id": sid, "runs": {}}
                for test_type in TEST_TYPES:
                    test_file = test_dir / "test_{}.py".format(test_type)
                    r = run_test_against_solution(
                        test_file, sol.code, sid, True, challenge.name,
                        template_path=challenge.template_path,
                    )
                    ok = _is_full_pass(r)
                    entry["runs"][test_type] = {
                        "executable": r.executable,
                        "passed": r.passed,
                        "failed": r.failed,
                        "errors": r.errors,
                        "total": r.total,
                        "full_pass": ok,
                        "error_label": r.error_label,
                        "error_detail": r.error_detail,
                        "pytest_output": (r.pytest_output or "")[:4500],
                    }
                cq.human_evaluations_all.append(entry)
                st = ", ".join(
                    "{}:{}".format(tt, "OK" if entry["runs"][tt]["full_pass"] else "FAIL")
                    for tt in TEST_TYPES
                )
                print("    {}  |  {}".format(sid, st))

        # Aggregate
        self._aggregate(cq)
        self._print_summary(cq)
        return cq

    # ── PER TEST FILE ─────────────────────────────────────────────────────

    def _evaluate_one_test_file(
        self,
        test_file:  Path,
        test_type:  str,
        challenge:  ChallengeInfo,
        human_sol:  HumanSolution,
        llm_sols:   List[LLMSolution],
        labels:     Dict[str, SolutionLabel],
    ) -> TestFileQuality:

        tfq = TestFileQuality(
            challenge=challenge.name,
            test_gen_model=self.test_gen_model,
            test_type=test_type,
        )

        # Run against human solution
        print("    Human solution ...", end=" ", flush=True)
        h_run = run_test_against_solution(
            test_file, human_sol.code,
            "{}/{}".format(human_sol.solution_set, human_sol.path.name),
            True, challenge.name,
            template_path=challenge.template_path,
        )
        tfq.human_run = h_run

        if not h_run.executable:
            tfq.error_label  = h_run.error_label
            tfq.error_detail = h_run.error_detail
            print("NOT EXECUTABLE -- {}: {}".format(
                h_run.error_label, h_run.error_detail[:60]))
        else:
            status = "PASS" if _is_full_pass(h_run) else "PARTIAL ({}/{})".format(
                h_run.passed, h_run.total)
            print("{} ({}/{})".format(
                "PASS" if _is_full_pass(h_run) else "FAIL",
                h_run.passed, h_run.total))
            if not _is_full_pass(h_run) and h_run.pytest_output:
                ex = h_run.pytest_output.strip()
                if len(ex) > 1200:
                    ex = ex[-1200:]
                print("    --- pytest excerpt ---\n    " + ex.replace("\n", "\n    "))

        # Record coverage + diversity (C_in on stripped body; see module docstring)
        try:
            src = test_file.read_text(encoding="utf-8", errors="replace")
            cin, lit, loop, n_asr = compute_coverage_inputs(src, challenge.test_cases)
            body = strip_injected_test_cases_block(src)
            tfq.coverage_inputs = cin
            tfq.coverage_literal = lit
            tfq.uses_test_cases_loop = loop
            tfq.n_assertions = n_asr
            tfq.diversity = compute_diversity(body, cin)
        except Exception:
            tfq.coverage_inputs = 0.0
            tfq.coverage_literal = 0.0
            tfq.uses_test_cases_loop = False
            tfq.n_assertions = 0
            tfq.diversity = 0.0

        # Run against each LLM solution if not human_only
        if not self.human_only:
            for sol in llm_sols:
                sid    = "{}/{}".format(sol.llm_model, sol.variant)
                label  = labels.get(sid, SolutionLabel(sid, None))
                llm_run = run_test_against_solution(
                    test_file, sol.code, sid,
                    label.is_correct, challenge.name,
                    template_path=challenge.template_path,
                )
                tfq.llm_runs.append(llm_run)

        # Compute scores + composite CQ
        tfq = compute_scores(tfq, human_only=self.human_only)
        tfq.cq = compute_composite_cq(tfq.tqs, tfq.coverage_inputs)

        cin_pct = tfq.coverage_inputs * 100
        if not self.human_only:
            print("    ES={:.2f}  CS={:.2f}  BDS={:.2f}  TQS={:.2f}  C_in={:.0f}%  CQ={:.2f}  Div={:.2f}  "
                  "(correct_pool={}/{}  wrong_caught={}/{})".format(
                tfq.es, tfq.cs, tfq.bds, tfq.tqs, cin_pct, tfq.cq, tfq.diversity,
                tfq.n_correct_pass, tfq.n_correct_total,
                tfq.n_wrong_fail, tfq.n_wrong_total,
            ))
        else:
            print("    ES={:.2f}  CS={:.2f}  C_in={:.0f}%  CQ={:.2f}  Div={:.2f}  (TQS=ES*CS)".format(
                tfq.es, tfq.cs, cin_pct, tfq.cq, tfq.diversity))
        return tfq

    # ── AGGREGATION ───────────────────────────────────────────────────────

    def _aggregate(self, cq: ChallengeQuality):
        files = cq.test_files
        if not files:
            return

        es_vals  = [f.es  for f in files]
        cs_vals  = [f.cs  for f in files]
        bds_vals = [f.bds for f in files]
        tqs_vals = [f.tqs for f in files]
        cin_vals = [f.coverage_inputs for f in files]
        lit_vals = [f.coverage_literal for f in files]
        cq_vals  = [f.cq for f in files]
        div_vals = [f.diversity for f in files]

        n = len(files)
        cq.avg_es  = sum(es_vals)  / n
        cq.avg_cs  = sum(cs_vals)  / n
        cq.avg_bds = sum(bds_vals) / n
        cq.avg_tqs = sum(tqs_vals) / n
        cq.avg_coverage_inputs = sum(cin_vals) / n
        cq.avg_cov_literal = sum(lit_vals) / n
        cq.avg_cq = sum(cq_vals) / n
        cq.avg_div = sum(div_vals) / n

        cq.scores_by_type = {
            f.test_type: {
                "es": round(f.es,  3),
                "cs": round(f.cs,  3),
                "bds": round(f.bds, 3),
                "tqs": round(f.tqs, 3),
                "coverage_inputs": round(f.coverage_inputs, 3),
                "coverage_literal": round(f.coverage_literal, 3),
                "uses_test_cases_loop": f.uses_test_cases_loop,
                "n_assertions": f.n_assertions,
                "cq": round(f.cq, 3),
                "diversity": round(f.diversity, 3),
                "n_correct_total": f.n_correct_total,
                "n_correct_pass":  f.n_correct_pass,
                "n_wrong_total":   f.n_wrong_total,
                "n_wrong_fail":    f.n_wrong_fail,
                "n_unknown":       f.n_unknown,
                "error_label":     f.error_label,
            }
            for f in files
        }

    def _print_summary(self, cq: ChallengeQuality):
        print("\n  Scores for {}:".format(cq.challenge))
        if not self.human_only:
            print("  {:<12} {:>6} {:>6} {:>6} {:>6} {:>6} {:>6} {:>6}".format(
                "Test type", "ES", "CS", "BDS", "TQS", "C_in", "CQ", "Div"))
            print("  " + "-" * 60)
            for f in cq.test_files:
                print("  {:<12} {:>5.2f} {:>5.2f} {:>5.2f} {:>5.2f} {:>5.0f}% {:>5.2f} {:>5.2f}".format(
                    f.test_type, f.es, f.cs, f.bds, f.tqs,
                    f.coverage_inputs * 100, f.cq, f.diversity))
            print("  " + "-" * 60)
            print("  {:<12} {:>5.2f} {:>5.2f} {:>5.2f} {:>5.2f} {:>5.0f}% {:>5.2f} {:>5.2f}".format(
                "AVERAGE",
                cq.avg_es, cq.avg_cs, cq.avg_bds, cq.avg_tqs,
                cq.avg_coverage_inputs * 100, cq.avg_cq, cq.avg_div))
        else:
            print("  {:<12} {:>6} {:>6} {:>6} {:>6} {:>6}".format(
                "Test type", "ES", "CS", "C_in", "CQ", "Div"))
            print("  " + "-" * 46)
            for f in cq.test_files:
                print("  {:<12} {:>5.2f} {:>5.2f} {:>5.0f}% {:>5.2f} {:>5.2f}".format(
                    f.test_type, f.es, f.cs, f.coverage_inputs * 100, f.cq, f.diversity))
            print("  " + "-" * 46)
            print("  {:<12} {:>5.2f} {:>5.2f} {:>5.0f}% {:>5.2f} {:>5.2f}".format(
                "AVERAGE", cq.avg_es, cq.avg_cs,
                cq.avg_coverage_inputs * 100, cq.avg_cq, cq.avg_div))


# ---------------------------------------------------------------------------
# JSON REPORT
# ---------------------------------------------------------------------------

def write_json_report(results: List[ChallengeQuality], out_path: Path):
    data = []
    for cq in results:
        data.append({
            "challenge":           cq.challenge,
            "test_gen_model":      cq.test_gen_model,
            "human_solution_used": cq.human_solution_used,
            "solution_correctness": {
                "n_total":   cq.n_llm_solutions,
                "n_correct": cq.n_correct_solutions,
                "n_wrong":   cq.n_wrong_solutions,
                "n_unknown": cq.n_unknown_solutions,
            },
            "scores": {
                "avg_es":  round(cq.avg_es,  3),
                "avg_cs":  round(cq.avg_cs,  3),
                "avg_bds": round(cq.avg_bds, 3),
                "avg_tqs": round(cq.avg_tqs, 3),
                "avg_coverage_inputs": round(cq.avg_coverage_inputs, 3),
                "avg_cq": round(cq.avg_cq, 3),
                "avg_cov_literal": round(cq.avg_cov_literal, 3),
                "avg_cov": round(cq.avg_coverage_inputs, 3),
                "avg_div": round(cq.avg_div, 3),
            },
            "human_evaluations_all": cq.human_evaluations_all,
            "scores_by_type": {
                tt: cq.scores_by_type.get(tt, {})
                for tt in TEST_TYPES
            },
            "llm_runs_detail": [
                {
                    "test_type":        f.test_type,
                    "human_run": {
                        "executable": f.human_run.executable if f.human_run else False,
                        "passed":     f.human_run.passed     if f.human_run else 0,
                        "failed":     f.human_run.failed     if f.human_run else 0,
                        "total":      f.human_run.total      if f.human_run else 0,
                        "error":      f.human_run.error_label if f.human_run else "",
                        "pytest_output": (f.human_run.pytest_output or "")[:4000]
                            if f.human_run else "",
                    },
                    "coverage_inputs": round(f.coverage_inputs, 3),
                    "coverage_literal": round(f.coverage_literal, 3),
                    "uses_test_cases_loop": f.uses_test_cases_loop,
                    "n_assertions": f.n_assertions,
                    "cq": round(f.cq, 3),
                    "coverage": round(f.coverage_inputs, 3),
                    "diversity": round(f.diversity, 3),
                    "llm_runs": [
                        {
                            "solution_id":      r.solution_id,
                            "solution_correct": r.solution_correct,
                            "executable":       r.executable,
                            "passed":           r.passed,
                            "failed":           r.failed,
                            "total":            r.total,
                            "error_label":      r.error_label,
                            "error_detail":     r.error_detail[:80],
                            "pytest_output":    (r.pytest_output or "")[:4000],
                        }
                        for r in f.llm_runs
                    ],
                }
                for f in cq.test_files
            ],
        })

    out_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print("  JSON -> {}".format(out_path.name))


# ---------------------------------------------------------------------------
# MARKDOWN REPORT
# ---------------------------------------------------------------------------

def _bar(v: float, w: int = 10) -> str:
    v = max(0.0, min(1.0, float(v)))
    return chr(9608) * round(v * w) + chr(9617) * (w - round(v * w))


def write_markdown_report(
    results: List[ChallengeQuality],
    out_path: Path,
    meta: Dict,
    human_only: bool,
):
    lines = [
        "# QHack 8-Challenge — Test Quality Evaluation Report",
        "",
        "**Generated:** {}".format(meta["generated_at"]),
        "**Test-generation model:** `{}`".format(meta["test_gen_model"]),
        "**Challenges evaluated:** {}".format(meta["n_challenges"]),
    ]
    if not human_only:
        lines.append("**LLM solution probes:** {}".format(", ".join(meta["llm_models"])))
    lines += ["", "---", "", "## Score Definitions", "",
        "Core correctness metrics (each in **[0.0 – 1.0]** except where noted):", "",
        "| Score | Full name | Meaning | Ideal |", "|-------|-----------|---------|-------|",
        "| **ES** | Executability Score | Test runs without crashing on the human baseline | 1.0 |",
        "| **CS** | Correctness Score | Fraction of oracle-*correct* solutions accepted | 1.0 |",
        "| **BDS** | Bug-Detection Score | Fraction of oracle-*wrong* solutions rejected | 1.0 |",
        "| **TQS** | Test Quality Score | ES × CS × BDS (full eval); ES × CS (human-only) | 1.0 |",
        "| **C_in** | Input coverage | Official inputs exercised in *LLM-written* test code (injected ``TEST_CASES`` block stripped); **1.0** if ``for ... in TEST_CASES`` | 1.0 |",
        "| **Cov_lit** | Literal coverage (diagnostic) | Same literal check on the *full* file — often ~1.0 because inputs appear in the injected list | — |",
        "| **CQ** | Composite | √(TQS × C_in) — balances discrimination and input exercise | 1.0 |",
        "| **Div** | Diversity | √(C_in × breadth); breadth = min(1, #``test_*`` / 3) | 1.0 |",
        "", "> **Human-only mode:** BDS is not defined; **TQS = ES × CS**.", "",
        "---", "", "## Solution Correctness (oracle labels)", "",
        "| Challenge | Total LLM | Correct | Wrong | Unknown |", "|-----------|----------:|-------:|------:|--------:|",
    ]
    for cq in results:
        lines.append("| {} | {} | {} | {} | {} |".format(
            cq.challenge, cq.n_llm_solutions,
            cq.n_correct_solutions, cq.n_wrong_solutions,
            cq.n_unknown_solutions))
    lines += ["", "---", "", "## Overall Scores by Challenge", "",
        "| Challenge | ES | CS | BDS | TQS | C_in | CQ | Div | Human baseline |",
        "|-----------|-----|-----|-----|-----|-----|-----|-----|---------------|",
    ]
    for cq in results:
        lines.append(
            "| **{}** | {:.2f} {} | {:.2f} {} | {:.2f} {} | **{:.2f}** {} | {:.2f} {} | {:.2f} {} | {:.2f} {} | {} |".format(
                cq.challenge,
                cq.avg_es,  _bar(cq.avg_es,  5),
                cq.avg_cs,  _bar(cq.avg_cs,  5),
                cq.avg_bds, _bar(cq.avg_bds, 5),
                cq.avg_tqs, _bar(cq.avg_tqs, 5),
                cq.avg_coverage_inputs, _bar(cq.avg_coverage_inputs, 5),
                cq.avg_cq, _bar(cq.avg_cq, 5),
                cq.avg_div, _bar(cq.avg_div, 5),
                cq.human_solution_used.split("/")[0],
            ))
    if results:
        avg = lambda f: sum(getattr(c, f) for c in results) / len(results)
        lines.append(
            "| **AVERAGE** | **{:.2f}** | **{:.2f}** | **{:.2f}** | **{:.2f}** | **{:.2f}** | **{:.2f}** | **{:.2f}** | — |".format(
                avg("avg_es"), avg("avg_cs"), avg("avg_bds"), avg("avg_tqs"),
                avg("avg_coverage_inputs"), avg("avg_cq"), avg("avg_div")))
    lines += ["", "---", "", "## Per-Challenge Detail", ""]
    for cq in results:
        lines += ["### {}".format(cq.challenge), ""]
        if not human_only:
            lines += [
                "| Test Type | ES | CS | BDS | TQS | C_in | CQ | Div | pool | wrong | err |",
                "|-----------|-----|-----|-----|-----|-----|-----|-----|------|-------|-----|",
            ]
            for f in cq.test_files:
                err = "`{}`".format(f.error_label) if f.error_label else "—"
                lines.append(
                    "| {} | {:.2f} | {:.2f} | {:.2f} | **{:.2f}** | {:.2f} | {:.2f} | {:.2f} | {}/{} | {}/{} | {} |".format(
                        f.test_type,
                        f.es, f.cs, f.bds, f.tqs,
                        f.coverage_inputs, f.cq, f.diversity,
                        f.n_correct_pass, f.n_correct_total,
                        f.n_wrong_fail, f.n_wrong_total,
                        err,
                    ))
        else:
            lines += [
                "| Test Type | ES | CS | C_in | CQ | Div | Error |",
                "|-----------|-----|-----|-----|-----|-----|-------|",
            ]
            for f in cq.test_files:
                err = "`{}`".format(f.error_label) if f.error_label else "—"
                lines.append(
                    "| {} | {:.2f} | {:.2f} | {:.2f} | {:.2f} | {:.2f} | {} |".format(
                        f.test_type, f.es, f.cs, f.coverage_inputs, f.cq, f.diversity, err))
        lines.append("")
    # Per LLM solution breakdown
    if not human_only:
        lines += ["---", "", "## LLM Solution Results (per challenge)", ""]
        for cq in results:
            lines += ["### {}".format(cq.challenge), ""]
            # Collect all solution IDs from first test file
            if not cq.test_files or not cq.test_files[0].llm_runs:
                continue
            sol_ids = [r.solution_id for r in cq.test_files[0].llm_runs]
            header = "| Test Type | " + " | ".join(sol_ids) + " |"
            sep    = "|-----------|" + "|".join(["---"] * len(sol_ids)) + "|"
            lines += [header, sep]
            for f in cq.test_files:
                run_map = {r.solution_id: r for r in f.llm_runs}
                row = "| {} |".format(f.test_type)
                for sid in sol_ids:
                    r = run_map.get(sid)
                    if r is None:
                        row += " — |"
                    elif not r.executable:
                        row += " CRASH |"
                    elif _is_full_pass(r):
                        tag = "✓PASS" if r.solution_correct is True else "⚠PASS"
                        row += " {} |".format(tag)
                    else:
                        tag = "REJECT" if r.solution_correct is False else "✗FAIL"
                        row += " {} |".format(tag)
                lines.append(row)
            lines.append("")
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print("  MD   -> {}".format(out_path.name))


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    framework_root = Path(FRAMEWORK_ROOT)

    parser = argparse.ArgumentParser(
        description="Evaluate quality of generated unit tests — "
                    "ES / CS / BDS / TQS scoring with optional human‑only mode",
    )
    parser.add_argument("--test-gen-model", default=DEFAULT_MODEL,
                        choices=list(MODELS.keys()))
    parser.add_argument("--llm-models", nargs="+", default=None, metavar="MODEL")
    parser.add_argument("--variants",   nargs="+", default=None, metavar="VARIANT")
    parser.add_argument("--only",       nargs="+", default=None, metavar="CHALLENGE")
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--root",       type=Path, default=framework_root)
    parser.add_argument("--human-only", action="store_true",
                        help="Evaluate only the human solutions (skip LLM probes)")
    parser.add_argument(
        "--prefer-human-set", type=str, default=None, metavar="FOLDER",
        help="Prefer human solutions under this subfolder of Human_solutions "
             "(e.g. Solution3). Used for picking baseline and --eval-all-human pool.",
    )
    parser.add_argument(
        "--eval-all-human", action="store_true",
        help="After scoring, run tests on every human solution in the pool "
             "(see --prefer-human-set) and record pass/fail + pytest excerpts.",
    )

    args    = parser.parse_args()
    root    = args.root.resolve()
    out_dir = args.output_dir or (root / "evaluation_results")
    out_dir.mkdir(parents=True, exist_ok=True)

    print("\n" + "=" * 65)
    print("  QHack 8-Challenge — Test Quality Evaluator")
    print("  Scores: ES · CS · BDS · TQS · C_in · CQ · Div")
    if args.human_only:
        print("  Mode: Human‑only (LLM probes skipped)")
    if args.prefer_human_set:
        print("  Prefer human set : {}".format(args.prefer_human_set))
    if args.eval_all_human:
        print("  Eval all human   : yes (per-solution report)")
    print("  Framework root   : {}".format(root))
    print("  Test-gen model   : {}".format(args.test_gen_model))
    if not args.human_only:
        print("  LLM probe models : {}".format(args.llm_models or LLM_SOLUTION_MODELS))
        print("  Variants         : {}".format(args.variants or LLM_SOLUTION_VARIANTS))
    print("  Challenges       : {}".format(args.only or "all 8"))
    print("  Output dir       : {}".format(out_dir))
    print("=" * 65)

    evaluator = TestQualityEvaluator(
        framework_root=root,
        test_gen_model=args.test_gen_model,
        llm_models=args.llm_models,
        variants=args.variants,
        only=args.only,
        human_only=args.human_only,
        prefer_human_set=args.prefer_human_set,
        eval_all_human=args.eval_all_human,
    )
    results = evaluator.run()

    if not results:
        print("\n  No results — run generate_tests.py first.")
        sys.exit(1)

    ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
    meta = {
        "generated_at":   datetime.now().isoformat(),
        "test_gen_model": args.test_gen_model,
        "n_challenges":   len(results),
        "llm_models":     args.llm_models or LLM_SOLUTION_MODELS,
    }

    print("\n[{}] Writing reports ...".format(6 if not args.human_only else 4))
    write_json_report(results,
                      out_dir / "test_quality_results_{}.json".format(ts))
    write_markdown_report(results,
                          out_dir / "test_quality_report_{}.md".format(ts), meta,
                          human_only=args.human_only)

    # ── Console summary ───────────────────────────────────────────────────
    print("\n" + "=" * 65)
    print("  FINAL QUALITY SCORES")
    print("=" * 65)
    if not args.human_only:
        print("  {:<22} {:>5} {:>5} {:>5} {:>5} {:>5} {:>5} {:>5}".format(
            "Challenge", "ES", "CS", "BDS", "TQS", "Cin%", "CQ", "Div"))
        print("  " + "-" * 62)
        for cq in results:
            print("  {:<22} {:>5.2f} {:>5.2f} {:>5.2f} {:>5.2f} {:>5.0f} {:>5.2f} {:>5.2f}".format(
                cq.challenge,
                cq.avg_es, cq.avg_cs, cq.avg_bds, cq.avg_tqs,
                cq.avg_coverage_inputs * 100, cq.avg_cq, cq.avg_div))
        if results:
            avg = lambda f: sum(getattr(c, f) for c in results) / len(results)
            print("  " + "-" * 62)
            print("  {:<22} {:>5.2f} {:>5.2f} {:>5.2f} {:>5.2f} {:>5.0f} {:>5.2f} {:>5.2f}".format(
                "AVERAGE",
                avg("avg_es"), avg("avg_cs"), avg("avg_bds"), avg("avg_tqs"),
                avg("avg_coverage_inputs") * 100, avg("avg_cq"), avg("avg_div")))
    else:
        print("  {:<22} {:>5} {:>5} {:>5} {:>5} {:>5}".format(
            "Challenge", "ES", "CS", "Cin%", "CQ", "Div"))
        print("  " + "-" * 48)
        for cq in results:
            print("  {:<22} {:>5.2f} {:>5.2f} {:>5.0f} {:>5.2f} {:>5.2f}".format(
                cq.challenge,
                cq.avg_es, cq.avg_cs, cq.avg_coverage_inputs * 100, cq.avg_cq, cq.avg_div))
        if results:
            avg = lambda f: sum(getattr(c, f) for c in results) / len(results)
            print("  " + "-" * 48)
            print("  {:<22} {:>5.2f} {:>5.2f} {:>5.0f} {:>5.2f} {:>5.2f}".format(
                "AVERAGE", avg("avg_es"), avg("avg_cs"),
                avg("avg_coverage_inputs") * 100, avg("avg_cq"), avg("avg_div")))
    print("=" * 65)


if __name__ == "__main__":
    main()