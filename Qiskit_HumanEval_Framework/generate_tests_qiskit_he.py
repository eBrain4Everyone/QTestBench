#!/usr/bin/env python3
"""
Generate syntactic / semantic / behavioural pytest files for Qiskit HumanEval
tasks (separate from PennyLane QHack). Uses OpenRouter like generate_tests.py.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from config import (
    MODELS,
    DEFAULT_MODEL,
    TEMPERATURE,
    DELAY_BETWEEN_CALLS,
    MAX_RETRIES,
    RETRY_DELAY,
    DEFAULT_LIMIT,
    MODEL_MAX_TOKENS,
    DEFAULT_MAX_TOKENS,
    MIN_RESPONSE_CHARS,
)
from openrouter_client import call_openrouter
from notebook_utils import strip_markdown_fences, check_syntax
from qiskit_he_common import (
    QISKIT_HE_FRAMEWORK_ROOT,
    GENERATED_TESTS_SUBDIR,
    CHECKPOINT_FILE_TEMPLATE,
    SCOPE_TASKS_FILENAME,
    load_tasks,
    official_check_injected_block,
    pending_bucket_counts,
    resolve_only_task_list,
    stratified_pick_tasks,
    QiskitHETask,
)

SYSTEM_PROMPT_QISKIT = """You are an expert quantum software engineer who writes \
pytest tests for Qiskit HumanEval-style tasks.

ABSOLUTE RULES:
1. Every test function MUST be self-contained: all imports inside the function body.
2. Load the candidate implementation from builtins:
     import builtins as _b
     sol = _b.INJECTED_SOLUTION_CODE   # full Python module source
     entry = _b.INJECTED_ENTRY_POINT    # str, function name to test
   Build namespace g = {"__builtins__": __builtins__} and exec(sol, g).
   Then candidate = g[entry]. Never embed the solution source in the test file.
3. The module-level OFFICIAL_CHECK_SOURCE (injected above your code) is the \
reference oracle string only; do not paste it as your test logic — write independent \
assertions that a correct solution should satisfy.
4. Use Qiskit / NumPy / SciPy as needed. Prefer stable public APIs.
5. Every assert must include a descriptive failure message string.
6. Generate EXACTLY 3 test functions named test_<descriptor>_1, _2, _3.
7. Return ONLY valid Python code — no markdown fences, no prose.
8. Use plain ASCII in code.

QUALITY (Correctness vs. bug detection):
- Correctness: assert only what the problem statement requires. Do not overfit to one \
reference style (e.g. unnecessary exact gate counts, global phase, or internal structure) \
unless the prompt explicitly demands it.
- Bug detection: each test should fail on plausible wrong implementations (wrong gate, \
wrong qubit/wire, wrong return type or shape, missing measurement when required).
- Numerics: use np.allclose(a, b, atol=1e-4, rtol=1e-5) (or looser atol if the prompt \
implies noisy/statistical outputs); avoid brittle exact float equality.
- Stochastic tests: if using Aer or sampling, use fixed seeds and small shot counts so \
results are stable across runs.
"""

HARNESS_NOTE = """After exec(sol, g), the callable under test is g[entry] where \
entry == INJECTED_ENTRY_POINT."""


def fmt_syntactic(t: QiskitHETask) -> str:
    return (
        f"Task folder name : {t.name}\n"
        f"Task id          : {t.task_id}\n"
        f"Entry point      : {t.entry_point}\n"
        f"Difficulty       : {t.difficulty_scale}\n\n"
        f"Problem prompt (excerpt):\n{t.prompt[:900]}\n\n"
        f"{HARNESS_NOTE}\n\n"
        "Generate 3 SYNTACTIC pytest tests.\n"
        "Focus: module loads, entry point exists and is callable, basic signature/plausibility.\n"
        "Verify: ast.parse(sol) succeeds; exec(sol, g) succeeds; "
        f"g['{t.entry_point}'] exists and is callable; inspect.signature if useful.\n"
        "Do not execute heavy simulators here — structure only.\n"
        "Still avoid assertions that only one specific implementation would satisfy; "
        "stick to interface and import-level checks.\n"
        "Return ONLY Python code.\n"
    )


def fmt_semantic(t: QiskitHETask) -> str:
    return (
        f"Task folder name : {t.name}\n"
        f"Entry point      : {t.entry_point}\n\n"
        f"Problem prompt:\n{t.prompt[:1200]}\n\n"
        f"{HARNESS_NOTE}\n\n"
        "Generate 3 SEMANTIC pytest tests.\n"
        "Exercise g[entry] with inputs implied by the prompt; use quantum_info, "
        "statevectors, operators, or counts as appropriate.\n"
        "Check observable properties from the spec (e.g. expected state, operator, "
        "distribution shape), not incidental implementation choices.\n"
        "Use np.allclose(..., atol=1e-4, rtol=1e-5) for floats; for complex vectors, "
        "compare up to global phase only if the spec allows equivalence modulo phase.\n"
        "Return ONLY Python code.\n"
    )


def fmt_behavioral(t: QiskitHETask) -> str:
    return (
        f"Task folder name : {t.name}\n"
        f"Entry point      : {t.entry_point}\n\n"
        f"Problem prompt:\n{t.prompt[:1200]}\n\n"
        f"{HARNESS_NOTE}\n\n"
        "Generate 3 BEHAVIOURAL end-to-end tests.\n"
        "If the task involves sampling or Aer, use a fixed seed and small shot counts; "
        "keep tests fast and deterministic.\n"
        "Assert outcomes at the level described in the prompt (counts, probabilities, "
        "final bits), tolerating small statistical noise where appropriate.\n"
        "Return ONLY Python code.\n"
    )


@dataclass
class GeneratedQHETests:
    task_name: str
    test_type: str
    model_key: str
    code: str
    is_valid_syntax: bool = True
    syntax_error: str = ""


def file_header(task_name: str, test_type: str, model_key: str) -> str:
    return (
        f"# {test_type.upper()} tests — Qiskit HumanEval task {task_name}\n"
        f"# Generated: {datetime.now().isoformat()}\n"
        f"# Model: {MODELS[model_key]} ({model_key})\n"
        f"# Framework: Qiskit HE (isolated from QHack)\n\n"
    )


def strip_duplicate_official_block(code: str) -> str:
    from qiskit_he_common import strip_injected_official_check_block

    if "# --- Official check block start" not in code:
        return code
    return strip_injected_official_check_block(code)


@dataclass
class _Ckpt:
    path: Path
    model_key: str
    data: Dict[str, Any] = field(default_factory=dict)

    def load(self) -> Dict[str, Any]:
        if self.path.exists():
            try:
                return json.loads(self.path.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {"model": self.model_key, "done": {}, "failed": {}}

    def save(self, d: Dict[str, Any]) -> None:
        self.path.write_text(json.dumps(d, indent=2), encoding="utf-8")


def run_generation(
    framework_root: Path,
    model_keys: List[str],
    only: Optional[List[str]] = None,
    resume: bool = True,
    dry_run: bool = False,
    limit: Optional[int] = None,
    stratify: Optional[Tuple[int, int, int, int]] = None,
) -> None:
    fs = str(framework_root).replace("\\", "/")
    if "..." in fs:
        print(
            "Error: --root must not contain literal '...' (that is not a path shortcut).\n"
            "  From this repo folder, use for example:\n"
            "    --root ./Framework_Qiskit_Human_Eval/full\n"
            "  or paste the full path ending in Framework_Qiskit_Human_Eval/full"
        )
        sys.exit(1)

    root = Path(framework_root).resolve()
    if not root.exists():
        print("No such path: {}".format(root))
        guess = Path.cwd() / "Framework_Qiskit_Human_Eval" / "full"
        if guess.exists() and guess != root:
            print("  Try instead: {}".format(guess))
            print("  (relative)   --root ./Framework_Qiskit_Human_Eval/full")
        else:
            print("  Use the folder that contains tasks/ and Human_solutions/, e.g.")
            print("    .../Framework_Qiskit_Human_Eval/full")
        sys.exit(1)
    tasks = load_tasks(root)
    if not tasks:
        from qiskit_he_common import TASKS_SUBDIR

        td = root / TASKS_SUBDIR
        print("No tasks loaded.")
        print("  Resolved --root: {}".format(root))
        print("  Expected task folders under: {}".format(td))
        if not td.is_dir():
            print("  That directory does not exist — check --root points to "
                  "Framework_Qiskit_Human_Eval/full or .../hard (not the parent).")
        else:
            n_dirs = sum(
                1 for p in td.iterdir()
                if p.is_dir() and p.name.startswith("task_")
            )
            print("  Found {} subdirs named task_* (need metadata.json + "
                  "reference_solution.py + official_check.py).".format(n_dirs))
        if "..." in str(framework_root):
            print("  Hint: do not use literal '...' in the path — paste the full path, e.g.")
            print("    C:/Users/<you>/.../Framework_Qiskit_Human_Eval/full")
        print("  If empty: python prepare_qiskit_human_eval.py")
        sys.exit(1)

    tlist = sorted(tasks.values(), key=lambda x: x.name)
    if only:
        tlist = [t for t in tlist if t.name in only]

    out_root = root / GENERATED_TESTS_SUBDIR
    print("\n" + "=" * 65)
    print("  Qiskit HumanEval — test generation")
    print(f"  Root: {root}")
    print(f"  Tasks in corpus: {len(tlist)}")
    if stratify is not None:
        e, m, h, a = stratify
        print(
            "  --stratify {}: each run picks (easy=basic {}, intermediate {}, "
            "hard=difficult {}, any {}) from pending".format(
                "{},{},{},{}".format(e, m, h, a), e, m, h, a
            )
        )
        if limit is not None:
            print("  (Note: --limit ignored when --stratify is set.)")
    elif limit is not None:
        print(f"  --limit {limit}: each run processes up to {limit} not-yet-done task(s)")
    print("  Resume: on by default (see checkpoint JSON); use --no-resume to ignore it")
    if not dry_run:
        print("  Generation mode: single-pass (no canonical validation / no repair loop)")
    if only is not None:
        print("  Task filter: {} tasks — {}".format(len(only), ", ".join(only[:8]) + (" …" if len(only) > 8 else "")))
    print("=" * 65)

    for mk in model_keys:
        ckpt_path = root / CHECKPOINT_FILE_TEMPLATE.format(model=mk)
        ck = _Ckpt(ckpt_path, mk)
        data = ck.load()
        pending_all = (
            [t for t in tlist if t.name not in data.get("done", {})]
            if resume
            else list(tlist)
        )
        strat_warnings: List[str] = []
        if stratify is not None:
            pending, strat_warnings = stratified_pick_tasks(
                pending_all, stratify[0], stratify[1], stratify[2], stratify[3]
            )
        elif limit is not None:
            pending = pending_all[:limit]
        else:
            pending = list(pending_all)

        if dry_run:
            bc = pending_bucket_counts(pending_all)
            print(
                f"  [{mk}] pending (not in checkpoint): {len(pending_all)} "
                f"| easy={bc['easy']} inter={bc['intermediate']} hard={bc['hard']} "
                f"unknown={bc['unknown']}"
            )
            for w in strat_warnings:
                print(f"    ! {w}")
            print(f"  [{mk}] would run this batch: {len(pending)} task(s)")
            if pending:
                sample = ", ".join(
                    "{}({})".format(t.name, t.difficulty_scale) for t in pending[:15]
                )
                if len(pending) > 15:
                    sample += ", …"
                print(f"      {sample}")
            continue

        for w in strat_warnings:
            print(f"  [{mk}] ! {w}")

        gen = _Generator(mk)
        for t in pending:
            print(f"  [{mk}] {t.name} ({t.task_id})")
            try:
                written = 0
                failures: List[str] = []
                for tt in ("syntactic", "semantic", "behavioral"):
                    gq, err = gen.generate_test_type(t, tt)
                    if not gq or not gq.code.strip():
                        if err:
                            failures.append("{}: {}".format(tt, err))
                        continue
                    dest = out_root / t.name / mk
                    dest.mkdir(parents=True, exist_ok=True)
                    (dest / f"test_{tt}.py").write_text(gq.code, encoding="utf-8")
                    written += 1
                    time.sleep(DELAY_BETWEEN_CALLS)
                if written == 3:
                    data.setdefault("done", {})[t.name] = {
                        "files": written,
                        "ts": datetime.now().isoformat(),
                    }
                    ck.save(data)
                elif written > 0:
                    data.setdefault("failed", {})[t.name] = (
                        "partial {}/3 — {}".format(written, "; ".join(failures) or "unknown")
                    )
                    ck.save(data)
                else:
                    data.setdefault("failed", {})[t.name] = (
                        "; ".join(failures) if failures else "empty"
                    )
                    ck.save(data)
            except KeyboardInterrupt:
                print("\n  Interrupted — checkpoint saved (completed tasks kept).")
                ck.save(data)
                break
            except Exception as e:
                data.setdefault("failed", {})[t.name] = str(e)
                print(f"    ERROR: {e}")
                ck.save(data)
        print(f"  [{mk}] checkpoint -> {ckpt_path.name}")


class _Generator:
    _FMT = {
        "syntactic": fmt_syntactic,
        "semantic": fmt_semantic,
        "behavioral": fmt_behavioral,
    }

    def __init__(self, model_key: str):
        self.model_key = model_key

    def _one(
        self,
        t: QiskitHETask,
        test_type: str,
        retry_feedback: Optional[str] = None,
    ) -> GeneratedQHETests:
        user = self._FMT[test_type](t)
        if retry_feedback:
            user = user + "\n\n" + retry_feedback
        raw = call_openrouter(
            user,
            model_key=self.model_key,
            system_prompt=SYSTEM_PROMPT_QISKIT,
        )
        if not raw:
            return GeneratedQHETests(t.name, test_type, self.model_key, "", False, "api fail")
        body = strip_markdown_fences(raw)
        body = strip_duplicate_official_block(body)
        inject = official_check_injected_block(t.entry_point, t.official_check)
        full = file_header(t.name, test_type, self.model_key) + inject + body
        ok, err = check_syntax(full)
        return GeneratedQHETests(
            t.name, test_type, self.model_key, full, ok, err or ""
        )

    def generate_test_type(
        self,
        t: QiskitHETask,
        test_type: str,
    ) -> Tuple[Optional[GeneratedQHETests], str]:
        """
        Returns (test, error summary) from a single LLM pass.
        This evaluation framework intentionally does not optimize generated tests
        with canonical validation or synthetic-negative repair during generation.
        """
        gq = self._one(t, test_type)
        if not gq.code.strip():
            return None, gq.syntax_error or "empty response"
        if not gq.is_valid_syntax:
            return None, gq.syntax_error or "syntax"
        return gq, ""


def task_names_from_model_checkpoint(framework_root: Path, reference_model: str) -> List[str]:
    """
    Sorted ``task_*`` names marked ``done`` in another model's checkpoint
    (for cross-model comparison on the same tasks).
    """
    ck_path = Path(framework_root) / CHECKPOINT_FILE_TEMPLATE.format(model=reference_model)
    if not ck_path.is_file():
        print(
            "Error: no checkpoint for model {!r} at {}".format(reference_model, ck_path),
            file=sys.stderr,
        )
        sys.exit(2)
    try:
        data = json.loads(ck_path.read_text(encoding="utf-8"))
    except Exception as e:
        print("Error: could not read checkpoint: {}".format(e), file=sys.stderr)
        sys.exit(2)
    done = data.get("done") or {}
    if not done:
        print(
            "Error: checkpoint has no completed tasks (empty 'done').",
            file=sys.stderr,
        )
        sys.exit(2)
    return sorted(done.keys())


def _parse_stratify(spec: str) -> Tuple[int, int, int, int]:
    parts = [p.strip() for p in spec.split(",") if p.strip() != ""]
    if len(parts) != 4:
        print(
            "Error: --stratify needs four integers: easy,intermediate,hard,any "
            "(e.g. 3,3,3,1). Dataset: basic, intermediate, difficult.",
            file=sys.stderr,
        )
        sys.exit(2)
    try:
        return (int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3]))
    except ValueError:
        print("Error: --stratify values must be integers.", file=sys.stderr)
        sys.exit(2)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate pytest tests for Qiskit HumanEval")
    parser.add_argument(
        "--root",
        type=Path,
        default=QISKIT_HE_FRAMEWORK_ROOT / "full",
        help="Prepared variant root (contains tasks/)",
    )
    parser.add_argument("--model", choices=list(MODELS.keys()))
    parser.add_argument("--models", nargs="+", choices=list(MODELS.keys()))
    parser.add_argument("--only", nargs="+", metavar="TASK", help="e.g. task_0000")
    parser.add_argument(
        "--only-file",
        type=Path,
        default=None,
        metavar="PATH",
        help="File with one task_* name per line (same format as evaluation_scope_tasks.txt).",
    )
    parser.add_argument(
        "--scoped",
        action="store_true",
        help="Restrict to tasks listed in {}/ under --root (fixed research set).".format(
            SCOPE_TASKS_FILENAME
        ),
    )
    parser.add_argument(
        "--same-tasks-as",
        metavar="MODEL_KEY",
        default=None,
        help="Use the same task folders as in another model's checkpoint "
        "(e.g. deepseekv32 after a stratify run). Combine with "
        "'--models gpt54 gemini3pro claudeopus46'. Do not pass --stratify.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        metavar="N",
        help="Process at most N tasks that are not yet in the checkpoint "
        "(default: all pending). Re-run with the same --limit to continue "
        "in order (task_0000, task_0001, …). Ignored if --stratify is set.",
    )
    parser.add_argument(
        "--stratify",
        nargs="?",
        const="3,3,3,1",
        default=None,
        metavar="E,M,H,A",
        help="Stratified batch from *pending* tasks: counts for "
        "easy (=basic), intermediate, hard (=difficult), then any remaining difficulty "
        "in stable task order. With no value, uses 3,3,3,1 (10 tasks). Overrides --limit.",
    )
    parser.add_argument("--no-resume", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.same_tasks_as and args.stratify is not None:
        print(
            "Error: use either --stratify or --same-tasks-as, not both.",
            file=sys.stderr,
        )
        sys.exit(2)

    if sum(bool(x) for x in (args.only, args.only_file, args.scoped, args.same_tasks_as)) > 1:
        print(
            "Error: use at most one of: --only, --only-file, --scoped, --same-tasks-as.",
            file=sys.stderr,
        )
        sys.exit(2)

    root_resolved = args.root.resolve()
    only_list: Optional[List[str]] = None
    if args.same_tasks_as:
        if args.same_tasks_as not in MODELS:
            print(
                "Error: --same-tasks-as must be a MODELS key in config.py, got {!r}.".format(
                    args.same_tasks_as
                ),
                file=sys.stderr,
            )
            sys.exit(2)
        ref_names = task_names_from_model_checkpoint(root_resolved, args.same_tasks_as)
        only_list = ref_names
        print(
            "Same-task set from checkpoint {} ({} tasks): {}".format(
                args.same_tasks_as,
                len(only_list),
                ", ".join(only_list[:12]) + (" …" if len(only_list) > 12 else ""),
            )
        )
    else:
        try:
            only_list, scope_note = resolve_only_task_list(
                root_resolved,
                list(args.only) if args.only else None,
                args.only_file,
                args.scoped,
            )
        except (FileNotFoundError, ValueError) as e:
            print("Error: {}".format(e), file=sys.stderr)
            sys.exit(2)
        if args.only or args.only_file or args.scoped:
            print("  Scope: {}".format(scope_note))

    strat = _parse_stratify(args.stratify) if args.stratify is not None else None

    mks = args.models or ([args.model] if args.model else [DEFAULT_MODEL])
    run_generation(
        root_resolved,
        mks,
        only=only_list,
        resume=not args.no_resume,
        dry_run=args.dry_run,
        limit=args.limit,
        stratify=strat,
    )


if __name__ == "__main__":
    main()
