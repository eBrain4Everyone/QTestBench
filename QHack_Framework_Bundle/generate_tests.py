"""
generate_tests.py
=================
Generates syntactic, semantic and behavioural pytest test suites for each
of the eight QHack challenges using a selected Large Language Model via
OpenRouter.

Design (v4):
* **No reference solution in prompts** — The LLM never sees the full
  template/reference implementation, only the challenge name, description
  excerpt, and official I/O pairs.  That prevents the model from pasting
  the official answer into the test file.
* **Injected ``TEST_CASES``** — After generation, the framework prepends the
  exact official ``TEST_CASES`` list so semantic/behavioural tests compare
  against ground-truth expected values (avoids hallucinated floats).
* **Injected solution at run time** — Tests load the candidate via
  ``builtins.INJECTED_SOLUTION_CODE`` (set by ``conftest.py`` during
  evaluation), not by embedding solution source in the test file.
* **Evaluation coverage (C_in)** — ``evaluate_solutions.py`` scores input
  exercise on the LLM-written part of the file (the injected ``TEST_CASES``
  block is stripped). Iterating ``for ... in TEST_CASES`` counts as full
  official coverage; literal overlap on the full file alone is only a
  diagnostic (often inflated toward 1.0).
"""

import os
import sys
import json
import re
import ast
import time
import argparse
import warnings
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime

import requests

from config import (
    OPENROUTER_URL,
    get_openrouter_api_key,
    MODELS, DEFAULT_MODEL,
    FRAMEWORK_ROOT,
    GENERATED_TESTS_SUBDIR,
    CHECKPOINT_FILE_TEMPLATE,
    NUM_TESTS_PER_TYPE, TEMPERATURE, MAX_CODE_CHARS,
    MAX_RETRIES, RETRY_DELAY, DELAY_BETWEEN_CALLS,
    DEFAULT_LIMIT, MODEL_MAX_TOKENS, DEFAULT_MAX_TOKENS,
    MIN_RESPONSE_CHARS, CHALLENGE_NAMES,
)
from challenge_mapper import ChallengeInfo, ChallengeMapper
from notebook_utils import strip_markdown_fences, check_syntax

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)


# ── SYSTEM PROMPT ─────────────────────────────────────────────────────────────

# The system prompt defines global rules that every generated test must obey.
# Compared to the original framework, rule 2 has been rewritten so that
# tests load the solution code from the evaluation harness via the
# builtins variable ``INJECTED_SOLUTION_CODE``.  This ensures that the
# tests exercise the candidate solution rather than the reference code.

SYSTEM_PROMPT = """You are an expert quantum computing engineer who writes \
high‑quality pytest test suites for PennyLane‑based quantum programs.

ABSOLUTE RULES — violating any of these makes a test useless:
1. Every test function MUST be 100 % self‑contained.
   - All imports (pennylane, numpy, json, ast, inspect, pytest, builtins, etc.)
     go INSIDE the test function body.
   - You MAY read the module-level ``TEST_CASES`` list (injected above your code)
     for official input/output pairs. Do NOT redefine ``TEST_CASES`` yourself.
2. Load the solution under test from the builtins variable ``INJECTED_SOLUTION_CODE``.
   - Inside the test function write ``import builtins as _b`` and then
     ``sol = _b.INJECTED_SOLUTION_CODE`` (a string of Python source).
   - Build a namespace with at least ``json``, ``qml`` and ``np`` and call
     ``exec(sol, namespace)``.
   - NEVER embed template, reference, or candidate solution source inside the test.
   - NEVER invent a local implementation — always execute the provided solution string.
3. For semantic/behavioural checks, use ONLY ``TEST_CASES`` for expected values
   (iterate ``for inp, exp in TEST_CASES:``). Never hard‑copy numeric expected
   arrays from memory — they must match ``TEST_CASES`` exactly.
4. Create ``qml.device(...)`` INSIDE each test function — never at module level.
5. Use only current PennyLane (>=0.38) API:
   - ``qml.StatePrep``  (NOT the deprecated ``qml.QubitStateVector``)
   - Do NOT access ``.tape``, ``.qtape``, ``circuit.tape``, ``dev.num_wires``,
     ``tape._ops``, or any private/deprecated attributes.
6. Every assert must include a descriptive failure‑message string.
7. Use ``np.allclose(a, b, atol=1e-4)`` for all floating‑point comparisons.
8. Generate EXACTLY 3 test functions, named ``test_<descriptor>_1/_2/_3``.
9. Return ONLY valid Python code — no markdown fences, no prose.
10. Use only plain ASCII — no Unicode math symbols in code.
11. The solution string is executed with ``exec()`` into a namespace containing
    ``json``, ``pennylane as qml``, ``pennylane.numpy as np``, ``__builtins__``.
    Then call ``ns["run"](test_input)`` with JSON string inputs from ``TEST_CASES``.
"""


# ── PROMPTS ───────────────────────────────────────────────────────────────────
# Prompts deliberately omit the reference implementation.  Only the
# challenge name, description, and official I/O pairs are provided.  The
# saved file will prepend a ``TEST_CASES`` literal so tests never rely on
# memorised numbers.

HARNESS_CONTRACT = """\
Standard QHack harness (your tests must assume this interface exists on the
candidate solution after ``exec()``:
  - def run(test_case_input: str) -> str
  - def check(solution_output: str, expected_output: str) -> None
Do not paste any solution implementation into the test file."""

SYNTACTIC_PROMPT = """\
Challenge : {name}

{harness_contract}

Official test cases (input JSON string -> expected JSON string) — the same
pairs will appear as the module-level ``TEST_CASES`` list in the generated file:
{test_cases_formatted}

Challenge description (excerpt):
{description}

Generate 3 SYNTACTIC pytest tests.

Purpose: verify that the solution code is structurally valid Python with the
correct function signatures.  Do NOT test quantum output here.

Each test must:
  1. Import ``ast``, ``inspect``, ``json``, ``pennylane as qml``,
     ``pennylane.numpy as np`` and ``builtins as _b`` INSIDE the function body.
  2. Retrieve the solution source via ``sol = _b.INJECTED_SOLUTION_CODE``.
  3. Call ``ast.parse(sol)`` and assert it succeeds.
  4. Build a namespace: ``ns = {{"json": json, "qml": qml, "np": np,
     "__builtins__": __builtins__}}``.
  5. Call ``exec(sol, ns)``.
  6. Assert that ``run`` and ``check`` exist in ``ns`` and are callable,
     with a descriptive message.
  7. Assert that the function signatures contain the expected parameter names
     using ``inspect.signature()`` (``run`` takes one str, ``check`` takes two str).

The 3 tests should check different structural aspects:
  test_1: syntax is valid Python and key functions exist
  test_2: function signatures have correct parameter names
  test_3: the run() and check() harness functions exist and are callable

Do NOT define ``TEST_CASES`` in your output — it is injected.

Return ONLY Python code. No markdown, no explanation.
"""

SEMANTIC_PROMPT = """\
Challenge : {name}

{harness_contract}

Official test cases (input -> expected):
{test_cases_formatted}

Challenge description:
{description}

Generate 3 SEMANTIC pytest tests.

PURPOSE AND CRITICAL RULE:
  Load the solution via ``exec()`` from ``INJECTED_SOLUTION_CODE``.
  Use ONLY the module-level ``TEST_CASES`` list for inputs and expected outputs.
  Do NOT invent expected values.  Do NOT write a local correct implementation.

Each test must:
  1. Import ``json``, ``pennylane as qml``, ``pennylane.numpy as np``,
     ``pytest`` and ``builtins as _b`` INSIDE the function body.
  2. ``sol = _b.INJECTED_SOLUTION_CODE`` then ``exec(sol, ns)`` with the
     standard namespace.
  3. Loop over ``TEST_CASES`` (or a subset per test) and compare
     ``run(inp)`` to ``exp`` using ``np.allclose`` on ``json.loads`` results.
  4. Each test function must cover at least 2 of the official test cases.

Test variety — the 3 tests should test different aspects:
  test_1: verify output values match expected for official cases
  test_2: verify output shape/type
  test_3: verify properties (e.g. probabilities sum to 1, valid range)

Do NOT define ``TEST_CASES`` in your output — it is injected.

Return ONLY Python code. No markdown, no explanation.
"""

BEHAVIORAL_PROMPT = """\
Challenge : {name}

{harness_contract}

Official test cases (input -> expected):
{test_cases_formatted}

Challenge description:
{description}

Generate 3 BEHAVIORAL pytest tests.

PURPOSE: End‑to‑end ``run()`` + ``check()`` using the module-level ``TEST_CASES``.

Each test must:
  1. Import ``json``, ``pennylane as qml``, ``pennylane.numpy as np``,
     ``pytest`` and ``builtins as _b`` INSIDE the function body.
  2. ``sol = _b.INJECTED_SOLUTION_CODE`` then ``exec(sol, ns)``.
  3. For each ``(inp, exp)`` in ``TEST_CASES``:
     ``output = ns["run"](inp)`` then ``ns["check"](output, exp)`` (catch failures).

Do NOT define ``TEST_CASES`` in your output — it is injected.

Return ONLY Python code. No markdown, no explanation.
"""


# ── DATA CLASSES ──────────────────────────────────────────────────────────────

@dataclass
class GeneratedTests:
    challenge_name: str
    test_type:      str
    model_key:      str
    code:           str
    test_cases:     List[Tuple[str, str]] = field(default_factory=list)
    is_valid_syntax: bool = True
    syntax_error:    str  = ""


# ── OPENROUTER CLIENT ─────────────────────────────────────────────────────────

def call_openrouter(
    prompt:         str,
    model_key:      str   = DEFAULT_MODEL,
    temperature:    float = TEMPERATURE,
    system_prompt:  Optional[str] = None,
) -> Optional[str]:

    model_id   = MODELS[model_key]
    max_tokens = MODEL_MAX_TOKENS.get(model_key, DEFAULT_MAX_TOKENS)
    sys_msg = system_prompt if system_prompt is not None else SYSTEM_PROMPT
    api_key = get_openrouter_api_key()
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type":  "application/json",
        "HTTP-Referer":  "https://github.com/qhack-framework",
        "X-Title":       "QHack 8-Challenge Framework",
    }
    payload = {
        "model":       model_id,
        "messages":    [
            {"role": "system", "content": sys_msg},
            {"role": "user",   "content": prompt},
        ],
        "temperature": temperature,
        "max_tokens":  max_tokens,
    }

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(f"        API call {attempt}/{MAX_RETRIES} [{model_id}] ...",
                  end=" ", flush=True)
            resp = requests.post(
                OPENROUTER_URL, headers=headers,
                json=payload, timeout=300,
            )
            resp.raise_for_status()
            data    = resp.json()
            content = data["choices"][0]["message"]["content"]
            finish  = data["choices"][0].get("finish_reason", "unknown")
            print(f"✓ ({len(content)} chars, finish={finish})")

            if finish == "length":
                print(f"        ⚠ WARNING: response truncated. "
                      f"Consider raising MODEL_MAX_TOKENS for '{model_key}'.")

            if len(content.strip()) < MIN_RESPONSE_CHARS:
                print(f"        ⚠ response too short "
                      f"({len(content.strip())} chars) — retrying ...")
                if attempt < MAX_RETRIES:
                    time.sleep(RETRY_DELAY)
                    continue
                print("        ✗ all retries returned short responses — skipping")
                return None

            return content

        except requests.exceptions.Timeout:
            print("✗ timeout")
        except requests.exceptions.HTTPError as e:
            code = e.response.status_code
            print(f"✗ HTTP {code}: {e.response.text[:120]}")
            if code in (400, 401, 403):
                return None
        except Exception as e:
            print(f"✗ {e}")

        if attempt < MAX_RETRIES:
            print(f"        retrying in {RETRY_DELAY}s ...")
            time.sleep(RETRY_DELAY)

    return None


# ── FILE HEADER ───────────────────────────────────────────────────────────────

def file_header(challenge_name: str, test_type: str, model_key: str) -> str:
    return (
        f"# {test_type.upper()} TESTS for {challenge_name}\n"
        f"# Generated  : {datetime.now().isoformat()}\n"
        f"# Challenge  : {challenge_name}\n"
        f"# Test type  : {test_type}\n"
        f"# Gen model  : {MODELS[model_key]} ({model_key})\n"
        f"# Strategy   : TEST_CASES injected + exec(INJECTED_SOLUTION_CODE)\n"
        f"# Auto‑generated by QHack 8‑Challenge Framework v4\n\n"
    )


def official_test_cases_block(test_cases: List[Tuple[str, str]]) -> str:
    """Python source defining TEST_CASES — prepended to each generated file."""
    if not test_cases:
        return (
            "# --- Official test cases (none in template) ---\n"
            "TEST_CASES = []\n\n"
        )
    lines = [
        "# --- Official test cases (injected by framework; do not edit) ---",
        "TEST_CASES = [",
    ]
    for inp, exp in test_cases:
        lines.append(f"    ({inp!r}, {exp!r}),")
    lines.append("]")
    lines.append("")
    return "\n".join(lines)


def strip_llm_duplicate_test_cases(code: str) -> str:
    """
    If the model ignored instructions and defined TEST_CASES, remove that
    assignment so only the framework-injected list remains.
    """
    m = re.search(r"^\s*TEST_CASES\s*=\s*\[", code, re.M)
    if not m:
        return code
    start_bracket = m.end() - 1
    depth = 0
    for i, ch in enumerate(code[start_bracket:], start_bracket):
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                return code[i + 1 :].lstrip("\n")
    return code


# ── TEST GENERATOR ────────────────────────────────────────────────────────────

class TestGenerator:

    _PROMPTS = {
        "syntactic":  SYNTACTIC_PROMPT,
        "semantic":   SEMANTIC_PROMPT,
        "behavioral": BEHAVIORAL_PROMPT,
    }

    def __init__(self, model_key: str = DEFAULT_MODEL):
        self.model_key = model_key

    def generate_all(self, challenge: ChallengeInfo) -> List[GeneratedTests]:
        results = []
        for test_type in ("syntactic", "semantic", "behavioral"):
            print(f"      [{test_type}]", end=" ", flush=True)
            gt = self._generate_one(challenge, test_type)
            results.append(gt)
            time.sleep(DELAY_BETWEEN_CALLS)
        return results

    def _generate_one(
        self, challenge: ChallengeInfo, test_type: str
    ) -> GeneratedTests:

        # Format test cases clearly for the prompt
        if challenge.test_cases:
            tc_formatted = "\n".join(
                f"  Test {i+1}: run({inp!r}) -> {exp!r}"
                for i, (inp, exp) in enumerate(challenge.test_cases)
            )
        else:
            tc_formatted = "  (No official test cases found in template)"

        prompt = self._PROMPTS[test_type].format(
            name=challenge.name,
            harness_contract=HARNESS_CONTRACT,
            description=challenge.description[:600],
            test_cases_formatted=tc_formatted,
        )

        tc_list = challenge.test_cases or []

        raw = call_openrouter(prompt, model_key=self.model_key)
        if raw is None:
            return GeneratedTests(
                challenge_name=challenge.name,
                test_type=test_type,
                model_key=self.model_key,
                code="",
                test_cases=tc_list,
                is_valid_syntax=False,
                syntax_error="API call failed",
            )

        body = strip_markdown_fences(raw)
        body = strip_llm_duplicate_test_cases(body)
        header = file_header(challenge.name, test_type, self.model_key)
        inject = official_test_cases_block(tc_list)
        full_code = header + inject + body
        valid, err = check_syntax(full_code)

        return GeneratedTests(
            challenge_name=challenge.name,
            test_type=test_type,
            model_key=self.model_key,
            code=full_code,
            test_cases=tc_list,
            is_valid_syntax=valid,
            syntax_error=err,
        )


# ── FILE SAVER ────────────────────────────────────────────────────────────────

def save_tests(tests: List[GeneratedTests], output_root: Path) -> int:
    written = 0
    for t in tests:
        if not t.code.strip():
            continue
        out_dir  = output_root / t.challenge_name / t.model_key
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"test_{t.test_type}.py"
        out_path.write_text(t.code, encoding="utf-8")
        written += 1
        if not t.is_valid_syntax:
            print(f"        ⚠ syntax warning for {out_path.name}: {t.syntax_error}")
    return written


# ── CHECKPOINT MANAGER ────────────────────────────────────────────────────────

class CheckpointManager:

    def __init__(self, path: Path, model_key: str):
        self.path      = path
        self.model_key = model_key
        self._data     = self._load()

    def _load(self) -> Dict[str, Any]:
        if self.path.exists():
            try:
                return json.loads(self.path.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {"model": self.model_key, "done": {}, "failed": {}}

    def _save(self):
        self.path.write_text(json.dumps(self._data, indent=2), encoding="utf-8")

    def _key(self, ch: ChallengeInfo) -> str:
        return ch.name

    def is_done(self, ch: ChallengeInfo) -> bool:
        return self._key(ch) in self._data.get("done", {})

    def mark_done(self, ch: ChallengeInfo, n: int):
        self._data.setdefault("done", {})[self._key(ch)] = {
            "files": n, "ts": datetime.now().isoformat()
        }
        self._save()

    def mark_failed(self, ch: ChallengeInfo, error: str):
        self._data.setdefault("failed", {})[self._key(ch)] = {
            "error": error, "ts": datetime.now().isoformat()
        }
        self._save()

    def reset(self):
        self._data = {"model": self.model_key, "done": {}, "failed": {}}
        self._save()
        print(f"  Checkpoint reset for model '{self.model_key}'.")

    def summary(self) -> str:
        done   = len(self._data.get("done", {}))
        failed = len(self._data.get("failed", {}))
        return f"{done} done, {failed} failed (out of {len(CHALLENGE_NAMES)} challenges)"


# ── PER‑MODEL RUNNER ──────────────────────────────────────────────────────────

def run_for_model(
    framework_root: Path,
    output_root:    Path,
    model_key:      str,
    challenges:     List[ChallengeInfo],
    limit:          Optional[int],
    resume:         bool,
    dry_run:        bool,
) -> List[Dict[str, Any]]:

    ckpt_path = framework_root / CHECKPOINT_FILE_TEMPLATE.format(model=model_key)
    ckpt      = CheckpointManager(ckpt_path, model_key)

    print(f"\n{'─' * 65}")
    print(f"  Test‑gen model : {MODELS[model_key]}  ({model_key})")
    print(f"{'─' * 65}")

    if resume:
        pending = [c for c in challenges if not ckpt.is_done(c)]
        skipped = len(challenges) - len(pending)
        if skipped:
            print(f"  Skipping {skipped} already‑completed challenge(s) (checkpoint).")
    else:
        pending = list(challenges)

    if limit is not None and len(pending) > limit:
        print(f"  Applying --limit {limit}: "
              f"will process {limit} of {len(pending)} pending.")
        pending = pending[:limit]

    total = len(pending)
    print(f"  Processing {total} challenge(s).\n")

    if dry_run:
        print("  [DRY RUN] Would process:")
        for c in pending:
            print(f"    {c.name}  (test_cases: {len(c.test_cases)})")
        return []

    generator = TestGenerator(model_key=model_key)
    results: List[Dict[str, Any]] = []

    for idx, ch in enumerate(pending, 1):
        print(f"  [{idx:>2}/{total}]  {ch.name}  "
              f"(test_cases: {len(ch.test_cases)})")
        try:
            tests   = generator.generate_all(ch)
            written = save_tests(tests, output_root)
            warns   = sum(
                1 for t in tests if not t.is_valid_syntax and t.code.strip()
            )
            if written == 0:
                ckpt.mark_failed(
                    ch, "No test files written (API error, empty response, or skip)")
                results.append({
                    "challenge":       ch.name,
                    "status":          "failed",
                    "error":           "no files written",
                    "files_written":   0,
                    "syntax_warnings": warns,
                })
            else:
                ckpt.mark_done(ch, written)
                results.append({
                    "challenge":       ch.name,
                    "status":          "ok",
                    "files_written":   written,
                    "syntax_warnings": warns,
                })
        except KeyboardInterrupt:
            print("\n  Interrupted — progress saved.")
            break
        except Exception as e:
            print(f"  ✗ FAILED: {e}")
            ckpt.mark_failed(ch, str(e))
            results.append({
                "challenge":       ch.name,
                "status":          "failed",
                "error":           str(e),
                "files_written":   0,
                "syntax_warnings": 0,
            })

    print(f"\n  [{model_key}] checkpoint: {ckpt.summary()}")
    return results


# ── STATUS DISPLAY ────────────────────────────────────────────────────────────

def show_status(framework_root: Path):
    print("\n" + "=" * 65)
    print("  CHECKPOINT STATUS (all test‑generation models)")
    print("=" * 65)
    any_found = False
    for mk in MODELS:
        ckpt_path = framework_root / CHECKPOINT_FILE_TEMPLATE.format(model=mk)
        if ckpt_path.exists():
            ckpt = CheckpointManager(ckpt_path, mk)
            print(f"  {mk:<14}  {ckpt.summary()}")
            any_found = True
    if not any_found:
        print("  No checkpoint files found — nothing has been run yet.")
    print("=" * 65)


# ── MAIN RUNNER ───────────────────────────────────────────────────────────────

def run(
    framework_root: Path,
    model_keys:     List[str],
    only:           Optional[List[str]] = None,
    resume:         bool = True,
    dry_run:        bool = False,
    limit:          Optional[int] = None,
):
    print("\n" + "=" * 65)
    print("  QHack 8‑Challenge — Unit Test Generator v2")
    print("  (exec()‑based using INJECTED_SOLUTION_CODE)")
    print(f"  Models      : {', '.join(model_keys)}")
    print(f"  Temperature : {TEMPERATURE}")
    print(f"  Limit       : {limit if limit is not None else 'all 8 challenges'}")
    print(f"  Resume      : {resume}")
    print(f"  Root        : {framework_root}")
    print("=" * 65)

    mapper = ChallengeMapper(str(framework_root))
    print("\n[1] Discovering challenges ...")
    ch_map = mapper.load_challenges()

    if not ch_map:
        print("  No challenges found. Check FRAMEWORK_ROOT in config.py.")
        sys.exit(1)

    challenges = list(ch_map.values())
    if only:
        challenges = [c for c in challenges if c.name in only]
        print(f"  After --only filter: {len(challenges)} challenge(s)")

    # Warn if any challenge has no test_cases (semantic/behavioural tests
    # will be less useful without official test cases to ground them)
    for ch in challenges:
        if not ch.test_cases:
            print(f"  ⚠  WARNING: {ch.name} has no test_cases — "
                  f"semantic/behavioral tests will be less reliable")

    output_root = framework_root / GENERATED_TESTS_SUBDIR

    print("\n[2] Generating tests ...")
    results_by_model: Dict[str, List[Dict[str, Any]]] = {}
    for mk in model_keys:
        results_by_model[mk] = run_for_model(
            framework_root=framework_root,
            output_root=output_root,
            model_key=mk,
            challenges=challenges,
            limit=limit,
            resume=resume,
            dry_run=dry_run,
        )

    if dry_run:
        print("\n[DRY RUN] No API calls made.")
        return

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    report = {"generated_at": datetime.now().isoformat(), "models": {}}
    for mk, results in results_by_model.items():
        report["models"][mk] = {
            "model_id":   MODELS[mk],
            "challenges": results,
            "totals": {
                "attempted":       len(results),
                "successful":      sum(1 for r in results if r["status"] == "ok"),
                "files_written":   sum(r.get("files_written", 0) for r in results),
                "syntax_warnings": sum(r.get("syntax_warnings", 0) for r in results),
            },
        }

    out = framework_root / f"generation_report_{ts}.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\n  Generation report -> {out.name}")
    print(f"\n  Next step:\n    python evaluate_solutions.py")


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    framework_root = Path(FRAMEWORK_ROOT)

    parser = argparse.ArgumentParser(
        description="Generate unit tests for the 8 QHack challenges via OpenRouter",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"Available models: {', '.join(MODELS.keys())}",
    )

    model_group = parser.add_mutually_exclusive_group()
    model_group.add_argument(
        "--model", choices=list(MODELS.keys()), help="Single model")
    model_group.add_argument(
        "--models", nargs="+", choices=list(MODELS.keys()), metavar="MODEL")

    parser.add_argument("--limit",     type=int, default=DEFAULT_LIMIT, metavar="N")
    parser.add_argument(
        "--only", nargs="+", default=None, metavar="CHALLENGE",
        help=f"Only these challenges. Choices: {CHALLENGE_NAMES}")
    parser.add_argument("--reset",     action="store_true")
    parser.add_argument("--no-resume", action="store_true")
    parser.add_argument("--dry-run",   action="store_true")
    parser.add_argument("--status",    action="store_true")
    parser.add_argument(
        "--root", type=Path, default=framework_root,
        help="Path to Framework_Eight_Challenges folder")

    args = parser.parse_args()
    root = args.root.resolve()

    if args.status:
        show_status(root)
        sys.exit(0)

    if args.models:
        model_keys = args.models
    elif args.model:
        model_keys = [args.model]
    else:
        model_keys = [DEFAULT_MODEL]

    if args.reset:
        for mk in model_keys:
            ckpt_path = root / CHECKPOINT_FILE_TEMPLATE.format(model=mk)
            CheckpointManager(ckpt_path, mk).reset()

    run(
        framework_root=root,
        model_keys=model_keys,
        only=args.only,
        resume=not args.no_resume,
        dry_run=args.dry_run,
        limit=args.limit,
    )


if __name__ == "__main__":
    main()