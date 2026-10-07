"""
run_pipeline.py
===============
One-shot runner: generates unit tests for all 8 challenges and then
immediately evaluates every LLM-generated solution against them,
comparing results with human (ground-truth) solutions.

Usage:
  python run_pipeline.py                        # full pipeline, default settings
  python run_pipeline.py --test-gen-model geminipro
  python run_pipeline.py --llm-models gemini gpt4.1
  python run_pipeline.py --only chalet_random_gate QSP_swamp
  python run_pipeline.py --skip-generation      # evaluation only (tests already exist)
  python run_pipeline.py --dry-run              # preview without API calls
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime

from config import (
    FRAMEWORK_ROOT, DEFAULT_MODEL, MODELS,
    LLM_SOLUTION_MODELS, LLM_SOLUTION_VARIANTS,
    CHALLENGE_NAMES, GENERATED_TESTS_SUBDIR,
)


def main():
    parser = argparse.ArgumentParser(
        description="Full pipeline: generate tests → evaluate LLM solutions for 8 challenges",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--test-gen-model", default=DEFAULT_MODEL, choices=list(MODELS.keys()),
        help=f"Model to use for test generation (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--llm-models", nargs="+", default=None,
        metavar="MODEL",
        help=f"LLM solution models to evaluate. Default: all. Choices: {LLM_SOLUTION_MODELS}",
    )
    parser.add_argument(
        "--variants", nargs="+", default=None,
        metavar="VARIANT",
        help=f"Solution variants. Default: all. Choices: {LLM_SOLUTION_VARIANTS}",
    )
    parser.add_argument(
        "--only", nargs="+", default=None,
        metavar="CHALLENGE",
        help=f"Restrict to these challenges. Choices: {CHALLENGE_NAMES}",
    )
    parser.add_argument(
        "--skip-generation", action="store_true",
        help="Skip test generation (use previously generated tests)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Preview test generation without calling the API",
    )
    parser.add_argument(
        "--no-resume", action="store_true",
        help="Ignore checkpoints and regenerate all tests",
    )
    parser.add_argument(
        "--root", type=Path, default=Path(FRAMEWORK_ROOT),
        help="Path to Framework_Eight_Challenges folder",
    )
    parser.add_argument(
        "--output-dir", type=Path, default=None,
        help="Output directory for evaluation reports",
    )

    args = parser.parse_args()
    root = args.root.resolve()

    print("\n" + "=" * 65)
    print("  QHack 8-Challenge — Full Pipeline")
    print(f"  Started   : {datetime.now().isoformat()}")
    print(f"  Root      : {root}")
    print(f"  Test model: {args.test_gen_model}")
    print("=" * 65)

    # ── STEP 1: Generate tests ────────────────────────────────────────────────
    if not args.skip_generation:
        print("\n" + "=" * 65)
        print("  STEP 1 OF 2: Generating unit tests")
        print("=" * 65)

        from generate_tests import run as generate_run
        generate_run(
            framework_root=root,
            model_keys=[args.test_gen_model],
            only=args.only,
            resume=not args.no_resume,
            dry_run=args.dry_run,
        )

        if args.dry_run:
            print("\n[DRY RUN] Stopping after generation preview.")
            return
    else:
        print("\n  [SKIP] Test generation skipped — using existing tests.")
        tests_root = root / GENERATED_TESTS_SUBDIR
        if not tests_root.exists():
            print(f"  ERROR: No generated tests found at {tests_root}")
            print("  Run without --skip-generation first.")
            sys.exit(1)

    # ── STEP 2: Evaluate solutions ────────────────────────────────────────────
    print("\n" + "=" * 65)
    print("  STEP 2 OF 2: Evaluating LLM solutions")
    print("=" * 65)

    from evaluate_solutions import (
        TestQualityEvaluator,
        write_json_report,
        write_markdown_report,
    )

    out_dir = args.output_dir or (root / "evaluation_results")
    out_dir.mkdir(parents=True, exist_ok=True)

    evaluator = TestQualityEvaluator(
        framework_root=root,
        test_gen_model=args.test_gen_model,
        llm_models=args.llm_models,
        variants=args.variants,
        only=args.only,
        human_only=False,
    )
    evals = evaluator.run()

    if not evals:
        print("\n  No evaluations performed.")
        sys.exit(1)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    meta = {
        "generated_at":   datetime.now().isoformat(),
        "test_gen_model": args.test_gen_model,
        "n_challenges":   len(evals),
        "llm_models":     args.llm_models or LLM_SOLUTION_MODELS,
    }

    write_json_report(evals, out_dir / f"evaluation_results_{ts}.json")
    write_markdown_report(
        evals, out_dir / f"evaluation_report_{ts}.md", meta, human_only=False,
    )

    print(f"\n  Reports written to: {out_dir}")
    print(f"  Pipeline complete at {datetime.now().isoformat()}")


if __name__ == "__main__":
    main()
