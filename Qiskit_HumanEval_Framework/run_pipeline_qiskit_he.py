#!/usr/bin/env python3
"""
End-to-end: generate tests (OpenRouter) then evaluate (Qiskit HE root).

Keeps all artifacts under Framework_Qiskit_Human_Eval/{full|hard}/ — never touches
Framework_Eight_Challenges.

Use ``--scoped`` so generation and evaluation both use the same task list from
``evaluation_scope_tasks.txt`` (e.g. 10 stratified tasks).
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

from config import DEFAULT_MODEL
from evaluate_solutions import write_json_report
from evaluate_qiskit_he import QiskitHETestQualityEvaluator
from generate_tests_qiskit_he import _parse_stratify, run_generation
from qiskit_he_common import (
    GENERATED_TESTS_SUBDIR,
    QISKIT_HE_FRAMEWORK_ROOT,
    resolve_only_task_list,
)


def main() -> None:
    p = argparse.ArgumentParser(description="Qiskit HumanEval — full pipeline")
    p.add_argument(
        "--root",
        type=Path,
        default=QISKIT_HE_FRAMEWORK_ROOT / "full",
        help="Variant root with tasks/ (run prepare_qiskit_human_eval.py first)",
    )
    p.add_argument("--test-gen-model", default=DEFAULT_MODEL)
    p.add_argument("--llm-models", nargs="+", default=None)
    p.add_argument("--variants", nargs="+", default=None)
    p.add_argument("--only", nargs="+", default=None)
    p.add_argument(
        "--only-file",
        type=Path,
        default=None,
        metavar="PATH",
        help="Task list file (one task_* per line).",
    )
    p.add_argument(
        "--scoped",
        action="store_true",
        help="Use evaluation_scope_tasks.txt under --root for generation and evaluation.",
    )
    p.add_argument("--limit", type=int, default=None)
    p.add_argument(
        "--stratify",
        nargs="?",
        const="3,3,3,1",
        default=None,
        metavar="E,M,H,A",
        help="Stratified batch (overrides --limit). Default 3,3,3,1 when flag present.",
    )
    p.add_argument("--skip-generation", action="store_true")
    p.add_argument("--human-only", action="store_true")
    p.add_argument("--use-synthetic-negatives", action="store_true")
    p.add_argument("--n-synthetic-negatives", type=int, default=3)
    p.add_argument("--no-resume", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--output-dir", type=Path, default=None)
    args = p.parse_args()
    root = args.root.resolve()

    if sum(bool(x) for x in (args.only, args.only_file, args.scoped)) > 1:
        print(
            "Error: use at most one of: --only, --only-file, --scoped.",
            file=sys.stderr,
        )
        sys.exit(2)

    try:
        only_tasks, scope_note = resolve_only_task_list(
            root,
            list(args.only) if args.only else None,
            args.only_file,
            args.scoped,
        )
    except (FileNotFoundError, ValueError) as e:
        print("Error: {}".format(e), file=sys.stderr)
        sys.exit(2)

    print("\n" + "=" * 65)
    print("  Qiskit HumanEval pipeline")
    print("  Root: {}".format(root))
    print("  Scope: {}".format(scope_note))
    if only_tasks:
        print("  Tasks: {}".format(", ".join(only_tasks)))
    print("=" * 65)

    strat = _parse_stratify(args.stratify) if args.stratify is not None else None

    if not args.skip_generation:
        run_generation(
            root,
            [args.test_gen_model],
            only=only_tasks,
            resume=not args.no_resume,
            dry_run=args.dry_run,
            limit=args.limit,
            stratify=strat,
        )
        if args.dry_run:
            return
    else:
        tests = root / GENERATED_TESTS_SUBDIR
        if not tests.is_dir():
            print("No generated_tests; run without --skip-generation first.")
            sys.exit(1)

    ev = QiskitHETestQualityEvaluator(
        framework_root=root,
        test_gen_model=args.test_gen_model,
        llm_models=args.llm_models,
        variants=args.variants,
        only=only_tasks,
        human_only=args.human_only,
        use_synthetic_negatives=args.use_synthetic_negatives,
        n_synthetic_negatives=max(0, int(args.n_synthetic_negatives)),
    )
    results = ev.run()
    if not results:
        print("No evaluation results.")
        sys.exit(1)

    if results:
        n = len(results)
        mean_es = sum(r.avg_es for r in results) / n
        mean_tqs = sum(r.avg_tqs for r in results) / n
        print(
            "\n--- Pipeline summary over {} task(s): mean ES={:.3f} mean TQS={:.3f} ---".format(
                n, mean_es, mean_tqs
            )
        )

    out = args.output_dir or (root / "evaluation_results")
    out.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = out / "test_quality_results_qiskit_he_{}.json".format(ts)
    write_json_report(results, path)
    print("\nWrote:", path)


if __name__ == "__main__":
    main()
