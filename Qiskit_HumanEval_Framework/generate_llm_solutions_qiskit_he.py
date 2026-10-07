#!/usr/bin/env python3
"""
Generate LLM solution files for Qiskit HumanEval tasks (optional probe pool).

Writes:
  Framework_Qiskit_Human_Eval/<variant>/LLM_generated_solutions/<model>/task_NNNN/<variant_name>.py

The evaluator labels each file with ``oracle_qiskit_he`` (CORRECT / WRONG / UNKNOWN).

Prompt uses only ``prompt.txt`` (stub + description) — not the canonical body — matching
the QHack-style separation between test generation inputs and ground-truth solutions.
"""

from __future__ import annotations

import argparse
import sys
import time
from datetime import datetime
from pathlib import Path

from config import (
    DEFAULT_MODEL,
    DELAY_BETWEEN_CALLS,
    MODELS,
    TEMPERATURE,
)
from notebook_utils import strip_markdown_fences
from openrouter_client import call_openrouter
from oracle_qiskit_he import run_oracle_on_files
from qiskit_he_common import (
    COHORT_SAMPLES_PER_TASK,
    LLM_SOLUTIONS_SUBDIR,
    QISKIT_HE_FRAMEWORK_ROOT,
    load_tasks,
    resolve_only_task_list,
)

SYSTEM_SOLVER = """You are an expert Qiskit programmer.
Return ONLY valid Python source code — a complete runnable module.
No markdown fences, no explanation.
The code must define the entry-point function named in the task.
Use compatible Qiskit public APIs."""


def _user_prompt(task_name: str, prompt_txt: str, entry_point: str, rag: bool) -> str:
    header = (
        f"Task folder: {task_name}\n"
        f"Entry point function name: {entry_point}\n\n"
        f"Complete the following program (fill in the function body and keep imports consistent):\n\n"
    )
    if rag:
        header += (
            "Use the task description and imports below. Prefer stable Qiskit APIs "
            "that match the installed qiskit version in a typical lab environment.\n\n"
        )
    return header + prompt_txt + "\n"


def _variant_plan(num_samples: int, with_rag: bool) -> list[tuple[str, bool]]:
    plan: list[tuple[str, bool]] = []
    for i in range(1, max(1, num_samples) + 1):
        plan.append((f"generated_non_rag_{i}", False))
    if with_rag:
        plan.append(("generated_rag_1", True))
    return plan


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate LLM solutions for Qiskit HE tasks")
    ap.add_argument(
        "--root",
        type=Path,
        default=QISKIT_HE_FRAMEWORK_ROOT / "full",
        help="Prepared variant root (contains tasks/)",
    )
    ap.add_argument("--model", default=DEFAULT_MODEL, choices=list(MODELS.keys()))
    ap.add_argument("--only", nargs="+", metavar="TASK", help="e.g. task_0000")
    ap.add_argument(
        "--only-file",
        type=Path,
        default=None,
        metavar="PATH",
        help="File with one task_* per line (same format as evaluation_scope_tasks.txt).",
    )
    ap.add_argument(
        "--scoped",
        action="store_true",
        help="Restrict to tasks listed in evaluation_scope_tasks.txt under --root.",
    )
    ap.add_argument("--limit", type=int, default=0, help="0 = all selected tasks")
    ap.add_argument(
        "--variant-name",
        default=None,
        help="Single filename stem (legacy). If set, overrides --num-samples.",
    )
    ap.add_argument(
        "--num-samples",
        type=int,
        default=COHORT_SAMPLES_PER_TASK,
        help="Generate generated_non_rag_1 .. generated_non_rag_N (default: %(default)s).",
    )
    ap.add_argument(
        "--with-rag",
        action="store_true",
        help="Also generate generated_rag_1 per task.",
    )
    ap.add_argument(
        "--temperature",
        type=float,
        default=None,
        help="Sampling temperature (default: config TEMPERATURE).",
    )
    ap.add_argument(
        "--label-oracle",
        action="store_true",
        help="After each write, run oracle_qiskit_he and print PASS/FAIL",
    )
    ap.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing generated solution files.",
    )
    args = ap.parse_args()

    root = Path(args.root).resolve()
    tasks = load_tasks(root)
    if not tasks:
        print("No tasks. Run: python prepare_qiskit_human_eval.py")
        sys.exit(1)

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

    tlist = sorted(tasks.values(), key=lambda t: t.name)
    if only_tasks:
        tlist = [t for t in tlist if t.name in only_tasks]
    if args.limit and args.limit > 0:
        tlist = tlist[: args.limit]

    if args.variant_name:
        variant_plan = [(args.variant_name, False)]
    else:
        variant_plan = _variant_plan(args.num_samples, args.with_rag)

    temp = args.temperature if args.temperature is not None else TEMPERATURE
    out_base = root / LLM_SOLUTIONS_SUBDIR / args.model
    print(f"Model: {args.model} -> {MODELS[args.model]}")
    print(f"Scope: {scope_note}")
    print(f"Tasks: {len(tlist)} | variants: {[v for v, _ in variant_plan]} | T={temp}")
    print(f"Output: {out_base}")

    for t in tlist:
        d = out_base / t.name
        d.mkdir(parents=True, exist_ok=True)
        for variant_name, use_rag in variant_plan:
            dest = d / f"{variant_name}.py"
            if dest.is_file() and not args.overwrite:
                print(f"  skip (exists): {dest}")
                continue

            user = _user_prompt(t.name, t.prompt, t.entry_point, use_rag)
            print(f"  {t.name} / {variant_name} ...", flush=True)
            raw = call_openrouter(
                user,
                model_key=args.model,
                system_prompt=SYSTEM_SOLVER,
                temperature=temp,
            )
            if not raw:
                print("    FAIL: no response")
                continue
            code = strip_markdown_fences(raw).strip() + "\n"
            header = (
                f"# LLM-generated solution — {t.name}\n"
                f"# Generated: {datetime.now().isoformat()}\n"
                f"# Model: {args.model}\n"
                f"# Variant: {variant_name}\n\n"
            )
            dest.write_text(header + code, encoding="utf-8")
            time.sleep(DELAY_BETWEEN_CALLS)

            if args.label_oracle:
                ok, detail = run_oracle_on_files(code, t.task_dir)
                st = "CORRECT" if ok is True else "WRONG" if ok is False else "UNKNOWN"
                print(f"    oracle -> {st}: {detail[:100]}")

    print("Done.")


if __name__ == "__main__":
    main()
