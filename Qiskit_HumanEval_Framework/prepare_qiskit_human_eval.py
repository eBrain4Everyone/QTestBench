#!/usr/bin/env python3
"""
Materialize Qiskit HumanEval JSON rows into a directory tree that mirrors the
QHack framework layout but stays under Framework_Qiskit_Human_Eval/{full,hard}/.

* full  — prompt includes imports + function stub (GitHub *dataset_qiskit_test_human_eval.json*).
* hard  — natural-language prompt + full canonical in JSON (*_hard.json*).

Run from the bundle directory:
  python prepare_qiskit_human_eval.py
  python prepare_qiskit_human_eval.py --only-variant hard
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

from qiskit_he_common import (
    QISKIT_HE_FRAMEWORK_ROOT,
    TASKS_SUBDIR,
    HUMAN_SOLUTIONS_SUBDIR,
    LLM_SOLUTIONS_SUBDIR,
    default_dataset_paths,
    normalize_official_test,
    reference_solution_format_label,
    reference_solution_from_dataset_row,
    sanity_check_reference_solution,
)


def materialize_variant(
    rows: List[Dict[str, Any]],
    variant: str,
    out_root: Path,
    human_set: str = "canonical",
) -> int:
    out_root = Path(out_root)
    tasks_root = out_root / TASKS_SUBDIR
    human_root = out_root / HUMAN_SOLUTIONS_SUBDIR / human_set
    llm_root = out_root / LLM_SOLUTIONS_SUBDIR

    tasks_root.mkdir(parents=True, exist_ok=True)
    human_root.mkdir(parents=True, exist_ok=True)
    llm_root.mkdir(parents=True, exist_ok=True)

    n = 0
    for i, row in enumerate(rows):
        task_folder = f"task_{i:04d}"
        d = tasks_root / task_folder
        d.mkdir(parents=True, exist_ok=True)

        official = normalize_official_test(row["test"])
        ref = reference_solution_from_dataset_row(row, variant)
        ok_ref, ref_msg = sanity_check_reference_solution(ref, row["entry_point"])
        if not ok_ref:
            raise ValueError(
                "Task {} ({}): invalid reference after assembly: {}".format(
                    i, row.get("task_id"), ref_msg
                )
            )

        meta = {
            "task_id": row["task_id"],
            "entry_point": row["entry_point"],
            "difficulty_scale": row.get("difficulty_scale", ""),
            "variant": variant,
            "index": i,
            "solution_format": reference_solution_format_label(variant),
        }
        (d / "metadata.json").write_text(
            json.dumps(meta, indent=2), encoding="utf-8"
        )
        (d / "prompt.txt").write_text(row.get("prompt", ""), encoding="utf-8")
        (d / "reference_solution.py").write_text(ref, encoding="utf-8")
        (d / "official_check.py").write_text(official, encoding="utf-8")

        hp = human_root / f"{task_folder}.py"
        hp.write_text(ref, encoding="utf-8")
        n += 1

    return n


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare Qiskit HumanEval task trees")
    df, dh = default_dataset_paths()
    parser.add_argument(
        "--full-json",
        type=Path,
        default=df,
        help="Path to dataset_qiskit_test_human_eval.json",
    )
    parser.add_argument(
        "--hard-json",
        type=Path,
        default=dh,
        help="Path to dataset_qiskit_test_human_eval_hard.json",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=QISKIT_HE_FRAMEWORK_ROOT,
        help="Framework_Qiskit_Human_Eval directory (creates full/ and hard/)",
    )
    parser.add_argument(
        "--only-variant",
        choices=("full", "hard", "both"),
        default="both",
    )
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)

    variants = (
        ("full", args.full_json),
        ("hard", args.hard_json),
    )
    if args.only_variant != "both":
        variants = [v for v in variants if v[0] == args.only_variant]

    print("Output root:", out)
    for variant, jpath in variants:
        jpath = jpath.resolve()
        if not jpath.is_file():
            print(f"  SKIP {variant}: missing {jpath}")
            continue
        rows = json.loads(jpath.read_text(encoding="utf-8"))
        target = out / variant
        n = materialize_variant(rows, variant, target)
        print(f"  {variant}: wrote {n} tasks under {target / TASKS_SUBDIR}")
        print(f"    human baseline -> {target / HUMAN_SOLUTIONS_SUBDIR / 'canonical'}")

    # Touch LLM dirs so structure is visible (optional)
    for variant in ("full", "hard"):
        if args.only_variant not in ("both", variant):
            continue
        llm = out / variant / LLM_SOLUTIONS_SUBDIR
        if llm.is_dir():
            placeholder = llm / ".gitkeep"
            if not placeholder.exists():
                placeholder.write_text(
                    "# Add: LLM_generated_solutions/<model>/task_NNNN/<variant>.py\n",
                    encoding="utf-8",
                )

    def _root_for_help(variant: str) -> str:
        # Forward slashes: avoids ugly line-wrap and any \U / \n confusion in consoles
        return (out / variant).resolve().as_posix()

    print("\nNext steps (run from this folder, same venv):")
    for variant in ("full", "hard"):
        if args.only_variant not in ("both", variant):
            continue
        rv = _root_for_help(variant)
        print("  [{}]".format(variant))
        print("    python generate_tests_qiskit_he.py --root {} --dry-run".format(rv))
        print("    python oracle_qiskit_he.py --root {} --limit 3".format(rv))


if __name__ == "__main__":
    main()
