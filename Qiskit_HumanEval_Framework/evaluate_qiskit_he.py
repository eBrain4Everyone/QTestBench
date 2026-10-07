#!/usr/bin/env python3
"""
Evaluate LLM-generated pytest suites for Qiskit HumanEval tasks (ES / CS / BDS / TQS),
mirroring evaluate_solutions.py but isolated under Framework_Qiskit_Human_Eval.
"""

from __future__ import annotations

import argparse
import ast
import re
import subprocess
import sys
import tempfile
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from config import DEFAULT_MODEL, MODELS
from evaluate_solutions import (
    ChallengeQuality,
    SingleRunResult,
    SolutionLabel,
    TestFileQuality,
    TEST_TYPES,
    _classify_error,
    _extract_error_detail,
    _is_full_fail,
    _is_full_pass,
    _parse_counts,
    _pytest_tail,
    compute_composite_cq,
    compute_coverage_literal,
    compute_diversity,
    compute_scores,
    count_pytest_assertions,
    write_json_report,
)
from oracle_qiskit_he import run_oracle_on_files
from qiskit_he_common import (
    QISKIT_HE_FRAMEWORK_ROOT,
    GENERATED_TESTS_SUBDIR,
    SCOPE_TASKS_FILENAME,
    LLM_SOLUTION_MODELS,
    LLM_SOLUTION_VARIANTS,
    official_strings_for_coverage,
    resolve_only_task_list,
    strip_injected_official_check_block,
    QiskitHETask,
)
from qiskit_he_mapper import (
    QiskitHEHumanSolution,
    QiskitHELLMSolution,
    QiskitHEMapper,
)


def determine_correctness_qhe(
    solution_code: str,
    task: QiskitHETask,
) -> Tuple[Optional[bool], str]:
    is_ok, detail = run_oracle_on_files(solution_code, task.task_dir)
    if is_ok is True:
        return True, detail
    if is_ok is False:
        return False, detail
    return None, detail


def build_synthetic_negative_candidates(
    base_code: str,
    max_candidates: int = 8,
) -> List[str]:
    """
    Produce deterministic, lightweight mutants from one trusted reference
    solution. We later keep only those that oracle-label as WRONG.
    """
    variants: List[str] = []

    def add(v: str):
        if v and v != base_code and v not in variants:
            variants.append(v)

    # 1) Return-None sabotage on first return.
    add(re.sub(r"(^\s*)return\s+.+$", r"\1return None", base_code, count=1, flags=re.M))

    # 2) Flip one strict comparison.
    add(base_code.replace("==", "!=", 1))

    # 3) Remove one measure_all call if present.
    add(re.sub(r"^\s*.*\.measure_all\(\)\s*$\n?", "", base_code, count=1, flags=re.M))

    # 4) Replace first CX by X (shape-preserving but behavior-changing often).
    add(base_code.replace(".cx(", ".x(", 1))

    # 5) Replace first H by X.
    add(base_code.replace(".h(", ".x(", 1))

    # 6) Perturb numeric constants slightly.
    add(re.sub(r"\b1000\b", "10", base_code, count=1))
    add(re.sub(r"\b100\b", "1", base_code, count=1))

    return variants[:max_candidates]


def sanitize_qiskit_test_source(src: str) -> str:
    """
    Repair common LLM truncation in generated tests, e.g.
    ``entry = _b.INJECTED_`` without ``ENTRY_POINT``.
    """
    src = re.sub(
        r"(\bentry\s*=\s*)_b\.INJECTED_\s*$",
        r"\1_b.INJECTED_ENTRY_POINT",
        src,
        flags=re.M,
    )
    src = re.sub(
        r"(\bentry\s*=\s*)_b\.INJECTED_\s*\n",
        r"\1_b.INJECTED_ENTRY_POINT\n",
        src,
    )
    return src


def make_synthetic_wrong_solutions(
    task: QiskitHETask,
    base_solution_code: str,
    target_wrong: int = 3,
    max_tries: int = 12,
) -> List[Tuple[str, str]]:
    """
    Return [(solution_id, code)] for mutants that the official oracle marks WRONG.
    """
    out: List[Tuple[str, str]] = []
    for i, cand in enumerate(build_synthetic_negative_candidates(base_solution_code, max_tries), 1):
        ok, _ = determine_correctness_qhe(cand, task)
        if ok is False:
            out.append(("synthetic_wrong/mutant_{:02d}".format(i), cand))
        if len(out) >= target_wrong:
            break
    return out


def run_qiskit_he_test(
    test_file: Path,
    solution_code: str,
    solution_id: str,
    solution_correct: Optional[bool],
    task_name: str,
    entry_point: str,
) -> SingleRunResult:
    result = SingleRunResult(
        solution_id=solution_id,
        solution_correct=solution_correct,
    )
    if not test_file.exists():
        result.error_label = "SYNTAX_ERROR"
        result.error_detail = "Test file does not exist"
        return result
    raw_src = test_file.read_text(encoding="utf-8", errors="replace")
    test_src = sanitize_qiskit_test_source(raw_src)
    try:
        ast.parse(test_src)
    except SyntaxError as e:
        result.error_label = "SYNTAX_ERROR"
        result.error_detail = "line {}: {}".format(e.lineno, e.msg)
        return result

    with tempfile.TemporaryDirectory(prefix="qiskit_he_eval_") as tmpdir:
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
            "_b.INJECTED_ENTRY_POINT = {!r}\n"
            "_b.INJECTED_CHALLENGE_NAME = {!r}\n".format(entry_point, task_name)
        )
        (tmp / "conftest.py").write_text(conftest, encoding="utf-8")
        try:
            proc = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pytest",
                    str(tmp / test_file.name),
                    "-v",
                    "--tb=short",
                    "--no-header",
                    "-q",
                    "--timeout=120",
                    "-p",
                    "no:warnings",
                ],
                capture_output=True,
                text=True,
                timeout=240,
                cwd=str(tmp),
            )
            output = proc.stdout + proc.stderr
        except subprocess.TimeoutExpired:
            result.error_label = "TIMEOUT"
            result.error_detail = "Whole-file timeout (240 s)"
            return result
        except Exception as e:
            result.error_label = "RUNTIME_ERROR"
            result.error_detail = str(e)[:200]
            return result

    passed, failed, errors = _parse_counts(output)
    total = passed + failed + errors
    result.executable = True
    result.passed = passed
    result.failed = failed
    result.errors = errors
    result.total = total

    if errors > 0 or total == 0:
        result.error_label = _classify_error(output)
        result.error_detail = _extract_error_detail(output)
        if result.error_label in ("IMPORT_ERROR", "RUNTIME_ERROR", "SYNTAX_ERROR"):
            result.executable = False

    if failed > 0 or errors > 0 or not result.executable:
        result.pytest_output = _pytest_tail(output, max_chars=5000)
    return result


_OC_LOOP = re.compile(r"for\s+[\w\s,()]+\s+in\s+OFFICIAL_CHECK_SOURCE\b", re.M)


def uses_official_check_loop(body: str) -> bool:
    return bool(_OC_LOOP.search(body))


def compute_coverage_inputs_qhe(
    full_src: str,
    official_check: str,
) -> Tuple[float, float, bool, int]:
    test_cases = official_strings_for_coverage(official_check)
    lit = compute_coverage_literal(full_src, test_cases)
    body = strip_injected_official_check_block(full_src)
    n_asr = count_pytest_assertions(body)
    if not test_cases:
        return 0.0, lit, False, n_asr
    if uses_official_check_loop(body):
        return 1.0, lit, True, n_asr
    cin = compute_coverage_literal(body, test_cases)
    return cin, lit, False, n_asr


def pick_best_human_solution_qhe(
    solutions: List[QiskitHEHumanSolution],
    test_dir: Path,
    task_name: str,
    entry_point: str,
    prefer_solution_set: Optional[str] = None,
) -> Optional[QiskitHEHumanSolution]:
    if not solutions:
        return None
    pool = solutions
    if prefer_solution_set:
        pref = [s for s in solutions if s.solution_set == prefer_solution_set]
        if pref:
            pool = pref
    test_files = list(test_dir.glob("test_*.py")) if test_dir.exists() else []
    if not test_files:
        return pool[0]

    best, best_score = None, -1
    for sol in pool:
        score = 0
        for tf in test_files[:3]:
            r = run_qiskit_he_test(
                tf, sol.code,
                "{}/{}".format(sol.solution_set, sol.path.name),
                True, task_name, entry_point,
            )
            score += r.passed
        if score > best_score:
            best_score = score
            best = sol
    return best


class QiskitHETestQualityEvaluator:
    def __init__(
        self,
        framework_root: Path,
        test_gen_model: str = DEFAULT_MODEL,
        llm_models: Optional[List[str]] = None,
        variants: Optional[List[str]] = None,
        only: Optional[List[str]] = None,
        human_only: bool = False,
        prefer_human_set: Optional[str] = None,
        use_synthetic_negatives: bool = False,
        n_synthetic_negatives: int = 3,
    ):
        self.framework_root = Path(framework_root)
        self.test_gen_model = test_gen_model
        self.tests_root = self.framework_root / GENERATED_TESTS_SUBDIR
        self.llm_models = llm_models or list(LLM_SOLUTION_MODELS)
        self.variants = variants or list(LLM_SOLUTION_VARIANTS)
        self.only = only
        self.human_only = human_only
        self.prefer_human_set = prefer_human_set
        self.use_synthetic_negatives = use_synthetic_negatives
        self.n_synthetic_negatives = max(0, int(n_synthetic_negatives))

    def run(self) -> List[ChallengeQuality]:
        mapper = QiskitHEMapper(self.framework_root)
        print("\n[1] Loading Qiskit HE tasks ...")
        tasks = mapper.load_tasks()
        if not tasks:
            print("  No tasks found.")
            return []

        print("\n[2] Loading human solutions ...")
        human_map = mapper.load_human_solutions()

        effective_human_only = self.human_only and not self.use_synthetic_negatives

        if not effective_human_only:
            print("\n[3] Loading LLM solutions ...")
            llm_map = mapper.load_llm_solutions(
                llm_models=self.llm_models,
                variants=self.variants,
            )
        else:
            llm_map = defaultdict(lambda: defaultdict(list))

        tlist = sorted(tasks.values(), key=lambda x: x.name)
        if self.only:
            tlist = [t for t in tlist if t.name in self.only]

        labels: Dict[str, Dict[str, SolutionLabel]] = {}
        if not effective_human_only:
            print("\n[4] Labelling LLM solutions (oracle) ...")
            for t in tlist:
                labels[t.name] = {}
                for m in self.llm_models:
                    for sol in llm_map[t.name].get(m, []):
                        sid = "{}/{}".format(sol.llm_model, sol.variant)
                        ok, det = determine_correctness_qhe(sol.code, t)
                        labels[t.name][sid] = SolutionLabel(sid, ok, det)
                        st = (
                            "CORRECT"
                            if ok is True
                            else "WRONG"
                            if ok is False
                            else "UNKNOWN"
                        )
                        print("    {} | {} -> {}  ({})".format(t.name, sid, st, det[:60]))
        else:
            for t in tlist:
                labels[t.name] = {}

        if self.use_synthetic_negatives:
            print(
                "\n[4b] Synthetic negatives enabled: target {} wrong mutant(s) per task "
                "(oracle-validated).".format(self.n_synthetic_negatives)
            )

        print("\n[5] Evaluating test quality ...")
        results: List[ChallengeQuality] = []
        for t in tlist:
            results.append(self._eval_task(t, human_map, llm_map, labels[t.name]))
        return results

    def _eval_task(
        self,
        task: QiskitHETask,
        human_map: Dict,
        llm_map: Dict,
        labels: Dict[str, SolutionLabel],
    ) -> ChallengeQuality:
        print("\n" + "-" * 65)
        print("  Task : {}".format(task.name))
        print("-" * 65)

        cq = ChallengeQuality(
            challenge=task.name,
            test_gen_model=self.test_gen_model,
        )
        test_dir = self.tests_root / task.name / self.test_gen_model
        all_human = human_map.get(task.name, [])
        human_sol = pick_best_human_solution_qhe(
            all_human, test_dir, task.name, task.entry_point,
            prefer_solution_set=self.prefer_human_set,
        )
        if human_sol is None:
            print("  WARNING: No human solution — skipping")
            return cq

        cq.human_solution_used = "{}/{}".format(
            human_sol.solution_set, human_sol.path.name)

        if not self.human_only:
            all_llm = [s for m in self.llm_models for s in llm_map[task.name].get(m, [])]
        else:
            all_llm = []

        synthetic_llm: List[QiskitHELLMSolution] = []
        if self.use_synthetic_negatives and self.n_synthetic_negatives > 0:
            synth = make_synthetic_wrong_solutions(
                task,
                human_sol.code,
                target_wrong=self.n_synthetic_negatives,
            )
            for sid, code in synth:
                # Reuse LLMSolution container for scoring pipeline compatibility.
                synthetic_llm.append(
                    QiskitHELLMSolution(
                        task_name=task.name,
                        llm_model="synthetic_wrong",
                        variant=sid.split("/", 1)[1] if "/" in sid else sid,
                        path=Path("<synthetic:{}>".format(sid)),
                        code=code,
                    )
                )
                labels[sid] = SolutionLabel(sid, False, "oracle_wrong")

        all_llm = all_llm + synthetic_llm

        cq.n_llm_solutions = len(all_llm)
        cq.n_correct_solutions = sum(
            1 for s in all_llm
            if labels.get("{}/{}".format(s.llm_model, s.variant), SolutionLabel("", None)).is_correct is True
        )
        cq.n_wrong_solutions = sum(
            1 for s in all_llm
            if labels.get("{}/{}".format(s.llm_model, s.variant), SolutionLabel("", None)).is_correct is False
        )
        cq.n_unknown_solutions = cq.n_llm_solutions - cq.n_correct_solutions - cq.n_wrong_solutions

        print("  Human baseline : {} (best of {})".format(
            cq.human_solution_used, len(all_human)))
        if (not self.human_only) or self.use_synthetic_negatives:
            print("  LLM solutions  : {} total | {} correct | {} wrong | {} unknown".format(
                cq.n_llm_solutions, cq.n_correct_solutions,
                cq.n_wrong_solutions, cq.n_unknown_solutions))
            if synthetic_llm:
                print("    (includes {} synthetic wrong probes)".format(len(synthetic_llm)))

        for test_type in TEST_TYPES:
            test_file = test_dir / "test_{}.py".format(test_type)
            print("\n  [{}]".format(test_type.upper()))
            tfq = self._one_file(
                test_file, test_type, task, human_sol, all_llm, labels)
            cq.test_files.append(tfq)

        self._aggregate(cq)
        self._print_summary(cq)
        return cq

    def _one_file(
        self,
        test_file: Path,
        test_type: str,
        task: QiskitHETask,
        human_sol: QiskitHEHumanSolution,
        llm_sols: List[QiskitHELLMSolution],
        labels: Dict[str, SolutionLabel],
    ) -> TestFileQuality:
        tfq = TestFileQuality(
            challenge=task.name,
            test_gen_model=self.test_gen_model,
            test_type=test_type,
        )
        print("    Human solution ...", end=" ", flush=True)
        h_run = run_qiskit_he_test(
            test_file, human_sol.code,
            "{}/{}".format(human_sol.solution_set, human_sol.path.name),
            True, task.name, task.entry_point,
        )
        tfq.human_run = h_run
        if not h_run.executable:
            tfq.error_label = h_run.error_label
            tfq.error_detail = h_run.error_detail
            print(
                "NOT EXECUTABLE -- {}: {}".format(
                    h_run.error_label or "RUNTIME_ERROR",
                    (h_run.error_detail or "")[:120],
                )
            )
            if h_run.pytest_output:
                ex = h_run.pytest_output.strip()
                if len(ex) > 1200:
                    ex = ex[-1200:]
                print("    --- pytest excerpt ---\n    " + ex.replace("\n", "\n    "))
        else:
            print("PASS" if _is_full_pass(h_run) else "FAIL", "({}/{})".format(
                h_run.passed, h_run.total))
            if not _is_full_pass(h_run) and h_run.pytest_output:
                ex = h_run.pytest_output.strip()
                if len(ex) > 1200:
                    ex = ex[-1200:]
                print("    --- pytest excerpt ---\n    " + ex.replace("\n", "\n    "))

        try:
            src = test_file.read_text(encoding="utf-8", errors="replace")
            cin, lit, loop, n_asr = compute_coverage_inputs_qhe(
                src, task.official_check)
            body = strip_injected_official_check_block(src)
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

        if not self.human_only or self.use_synthetic_negatives:
            for sol in llm_sols:
                sid = "{}/{}".format(sol.llm_model, sol.variant)
                lab = labels.get(sid, SolutionLabel(sid, None))
                tfq.llm_runs.append(
                    run_qiskit_he_test(
                        test_file, sol.code, sid,
                        lab.is_correct, task.name, task.entry_point,
                    )
                )

        tfq = compute_scores(tfq, human_only=(self.human_only and not self.use_synthetic_negatives))
        tfq.cq = compute_composite_cq(tfq.tqs, tfq.coverage_inputs)
        print("    ES={:.2f} CS={:.2f} BDS={:.2f} TQS={:.2f} C_in={:.0f}% CQ={:.2f}".format(
            tfq.es, tfq.cs, tfq.bds, tfq.tqs,
            tfq.coverage_inputs * 100, tfq.cq))
        return tfq

    def _aggregate(self, cq: ChallengeQuality) -> None:
        files = cq.test_files
        if not files:
            return
        n = len(files)
        cq.avg_es = sum(f.es for f in files) / n
        cq.avg_cs = sum(f.cs for f in files) / n
        cq.avg_bds = sum(f.bds for f in files) / n
        cq.avg_tqs = sum(f.tqs for f in files) / n
        cq.avg_coverage_inputs = sum(f.coverage_inputs for f in files) / n
        cq.avg_cov_literal = sum(f.coverage_literal for f in files) / n
        cq.avg_cq = sum(f.cq for f in files) / n
        cq.avg_div = sum(f.diversity for f in files) / n
        cq.scores_by_type = {
            f.test_type: {
                "es": round(f.es, 3),
                "cs": round(f.cs, 3),
                "bds": round(f.bds, 3),
                "tqs": round(f.tqs, 3),
                "coverage_inputs": round(f.coverage_inputs, 3),
                "cq": round(f.cq, 3),
                "diversity": round(f.diversity, 3),
            }
            for f in files
        }

    def _print_summary(self, cq: ChallengeQuality) -> None:
        print("\n  Averages for {}: ES={:.2f} CS={:.2f} TQS={:.2f} C_in={:.0f}%".format(
            cq.challenge, cq.avg_es, cq.avg_cs, cq.avg_tqs,
            cq.avg_coverage_inputs * 100))


def write_qiskit_he_summary_report(
    results: List[ChallengeQuality],
    out_path: Path,
    meta: Dict[str, Any],
    human_only: bool,
) -> None:
    """Compact markdown summary (scoped-slice friendly)."""
    n = len(results)
    if n == 0:
        return

    def mean(attr: str) -> float:
        return sum(getattr(r, attr) for r in results) / n

    lines = [
        "# Qiskit HumanEval — Test Quality Evaluation Report",
        "",
    ]
    if meta.get("validation_config_title"):
        lines.append(
            "**Validation configuration:** {}".format(meta["validation_config_title"])
        )
        if meta.get("validation_config_subtitle"):
            lines.append("")
            lines.append("*{}*".format(meta["validation_config_subtitle"]))
        lines.append("")
    lines += [
        "**Test-generation model:** `{}`".format(meta.get("test_gen_model", "")),
        "**Tasks evaluated:** {}".format(n),
    ]
    if meta.get("source_json"):
        lines.append("**Source JSON:** `{}`".format(meta["source_json"]))
    lines += [
        "",
        "---",
        "",
        "## Mean scores (scoped slice)",
        "",
        "| Metric | Mean |",
        "|--------|------|",
        "| ES | {:.3f} |".format(mean("avg_es")),
        "| CS | {:.3f} |".format(mean("avg_cs")),
        "| BDS | {:.3f} |".format(mean("avg_bds")),
        "| TQS | {:.3f} |".format(mean("avg_tqs")),
        "| CQ | {:.3f} |".format(mean("avg_cq")),
        "| C_in | {:.3f} |".format(mean("avg_coverage_inputs")),
        "",
    ]
    if human_only:
        lines.append("> Human-only mode: BDS omitted; **TQS = ES × CS**.")
    else:
        lines.append("> Full cohort: **TQS = ES × CS × BDS**.")
    lines += [
        "",
        "> Full per-task breakdown: see the JSON file above.",
        "",
    ]
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print("  MD   -> {}".format(out_path.name))


def main() -> None:
    ap = argparse.ArgumentParser(description="Evaluate Qiskit HE generated tests")
    ap.add_argument(
        "--root",
        type=Path,
        default=QISKIT_HE_FRAMEWORK_ROOT / "full",
    )
    ap.add_argument("--test-gen-model", default=DEFAULT_MODEL)
    ap.add_argument("--llm-models", nargs="+", default=None)
    ap.add_argument("--variants", nargs="+", default=None)
    ap.add_argument("--only", nargs="+", default=None)
    ap.add_argument(
        "--only-file",
        type=Path,
        default=None,
        metavar="PATH",
        help="File with one task_* per line (overrides evaluating all corpus tasks).",
    )
    ap.add_argument(
        "--scoped",
        action="store_true",
        help="Evaluate only tasks listed in {}/ under --root.".format(SCOPE_TASKS_FILENAME),
    )
    ap.add_argument("--human-only", action="store_true")
    ap.add_argument(
        "--use-synthetic-negatives",
        action="store_true",
        help="Build oracle-validated wrong probes by mutating canonical solution "
             "for each task. Enables BDS/TQS-style discrimination even when "
             "LLM_generated_solutions is empty.",
    )
    ap.add_argument(
        "--n-synthetic-negatives",
        type=int,
        default=3,
        help="Target number of synthetic wrong probes per task "
             "(default: 3, used with --use-synthetic-negatives).",
    )
    ap.add_argument("--output-dir", type=Path, default=None)
    ap.add_argument(
        "--validation-config",
        choices=["1", "2", "3"],
        default=None,
        help="Preset cohort: 1=human only, 2=human+LLM, 3=human+synthetic.",
    )
    args = ap.parse_args()

    validation_meta: Dict[str, str] = {}
    if args.validation_config:
        repo_root = Path(__file__).resolve().parent.parent
        sys.path.insert(0, str(repo_root))
        from validation_configs import VALIDATION_CONFIGS  # noqa: WPS433

        vcfg = VALIDATION_CONFIGS[args.validation_config]
        validation_meta = {
            "validation_config_key": vcfg.key,
            "validation_config_title": vcfg.title,
            "validation_config_subtitle": vcfg.subtitle,
        }
        if vcfg.key == "1":
            args.scoped = True
            args.human_only = True
            args.use_synthetic_negatives = False
        elif vcfg.key == "2":
            args.scoped = True
            args.human_only = False
            args.use_synthetic_negatives = False
        elif vcfg.key == "3":
            args.scoped = True
            args.human_only = True
            args.use_synthetic_negatives = True
            if args.n_synthetic_negatives == 3:
                args.n_synthetic_negatives = vcfg.n_synthetic_negatives

    if sum(bool(x) for x in (args.only, args.only_file, args.scoped)) > 1:
        print(
            "Error: use at most one of: --only, --only-file, --scoped.",
            file=sys.stderr,
        )
        sys.exit(2)

    root = args.root.resolve()
    try:
        only_tasks, scope_note = resolve_only_task_list(
            root,
            args.only,
            args.only_file,
            args.scoped,
        )
    except (FileNotFoundError, ValueError) as e:
        print("Error: {}".format(e), file=sys.stderr)
        sys.exit(2)

    print("\nEvaluation scope: {}".format(scope_note))
    if only_tasks:
        print("  Tasks: {}".format(", ".join(only_tasks)))

    out_dir = (args.output_dir or (root / "evaluation_results")).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    effective_human_only = args.human_only and not args.use_synthetic_negatives
    if validation_meta.get("validation_config_title"):
        print("Validation configuration:", validation_meta["validation_config_title"])

    ev = QiskitHETestQualityEvaluator(
        framework_root=root,
        test_gen_model=args.test_gen_model,
        llm_models=args.llm_models,
        variants=args.variants,
        only=only_tasks,
        human_only=args.human_only,
        use_synthetic_negatives=args.use_synthetic_negatives,
        n_synthetic_negatives=args.n_synthetic_negatives,
    )
    results = ev.run()
    if not results:
        sys.exit(1)
    if results:
        n = len(results)
        mean_es = sum(r.avg_es for r in results) / n
        mean_tqs = sum(r.avg_tqs for r in results) / n
        print(
            "\n--- Summary over {} task(s): mean ES={:.3f} mean TQS={:.3f} ---".format(
                n, mean_es, mean_tqs
            )
        )
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_name = "test_quality_results_qiskit_he_{}.json".format(ts)
    json_path = out_dir / json_name
    write_json_report(results, json_path)
    try:
        source_json = str(json_path.resolve().relative_to(root.resolve())).replace(
            "\\", "/"
        )
    except ValueError:
        source_json = json_path.name
    meta = {
        "test_gen_model": args.test_gen_model,
        "source_json": source_json,
        **validation_meta,
    }
    write_qiskit_he_summary_report(
        results,
        out_dir / "test_quality_report_qiskit_he_{}.md".format(ts),
        meta,
        human_only=effective_human_only,
    )
    print("\nWrote:", json_path)


if __name__ == "__main__":
    main()
