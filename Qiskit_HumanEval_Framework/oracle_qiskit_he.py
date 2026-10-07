#!/usr/bin/env python3
"""
Oracle for Qiskit HumanEval tasks: execute reference (or any) solution + official
``check(candidate)`` in one shared namespace (arXiv:2406.14712-style pass/fail).
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Optional, Tuple

from qiskit_he_common import load_tasks

_HARNESS = r'''
import json, sys, warnings, traceback
warnings.filterwarnings("ignore")

META = json.load(open("metadata.json", encoding="utf-8"))
ENTRY = META["entry_point"]
solution = open("solution_under_test.py", encoding="utf-8").read()
check_src = open("official_check.py", encoding="utf-8").read()

g = {"__name__": "__oracle__", "__builtins__": __builtins__}
try:
    exec(compile(solution, "<solution>", "exec"), g)
except Exception as e:
    print("LOAD_ERROR:" + repr(e)[:200])
    sys.exit(2)

if ENTRY not in g:
    print("MISSING_ENTRY:" + ENTRY)
    sys.exit(2)

candidate = g[ENTRY]

try:
    exec(compile(check_src, "<check>", "exec"), g)
except Exception as e:
    print("CHECK_LOAD_ERROR:" + repr(e)[:200])
    sys.exit(2)

fn = g.get("check")
if not callable(fn):
    print("MISSING_CHECK")
    sys.exit(2)

try:
    fn(candidate)
except AssertionError as e:
    print("FAILED:" + str(e)[:120])
    sys.exit(1)
except Exception as e:
    print("ERROR:" + repr(e)[:200])
    traceback.print_exc()
    sys.exit(2)

print("PASSED")
sys.exit(0)
'''


def run_oracle_on_files(
    solution_text: str,
    task_dir: Path,
    timeout: int = 120,
) -> Tuple[Optional[bool], str]:
    task_dir = Path(task_dir)
    with tempfile.TemporaryDirectory(prefix="qiskit_he_oracle_") as tmp:
        t = Path(tmp)
        (t / "solution_under_test.py").write_text(solution_text, encoding="utf-8")
        (t / "official_check.py").write_text(
            (task_dir / "official_check.py").read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        (t / "metadata.json").write_text(
            (task_dir / "metadata.json").read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        (t / "_run.py").write_text(_HARNESS, encoding="utf-8")
        try:
            p = subprocess.run(
                [sys.executable, str(t / "_run.py")],
                cwd=str(t),
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            out = (p.stdout or "") + (p.stderr or "")
        except subprocess.TimeoutExpired:
            return None, "oracle_timeout"

    if "PASSED" in out and p.returncode == 0:
        return True, "ok"
    if p.returncode == 1 or "FAILED" in out:
        return False, out.strip()[:200]
    # Runtime / load failures: solution does not satisfy official_check(candidate).
    # Label as WRONG so Config~2 cohort probes count toward CS/BDS (not UNKNOWN).
    if (
        "ERROR:" in out
        or "LOAD_ERROR" in out
        or "MISSING_ENTRY" in out
        or "MISSING_CHECK" in out
        or "CHECK_LOAD_ERROR" in out
        or p.returncode != 0
    ):
        return False, out.strip()[:200]
    return None, out.strip()[:200]


def main() -> None:
    from qiskit_he_common import QISKIT_HE_FRAMEWORK_ROOT

    ap = argparse.ArgumentParser(description="Run Qiskit HE oracle on reference solutions")
    ap.add_argument(
        "--root",
        type=Path,
        default=QISKIT_HE_FRAMEWORK_ROOT / "full",
        help="Prepared variant root (contains tasks/)",
    )
    ap.add_argument("--limit", type=int, default=0, help="0 = all tasks")
    ap.add_argument("--only", nargs="+", help="Task folder names, e.g. task_0000")
    args = ap.parse_args()

    tasks = load_tasks(args.root)
    if not tasks:
        print("No tasks found. Run: python prepare_qiskit_human_eval.py")
        sys.exit(1)

    names = sorted(tasks.keys())
    if args.only:
        names = [n for n in names if n in args.only]
    if args.limit and args.limit > 0:
        names = names[: args.limit]

    ok = fail = err = 0
    for name in names:
        t = tasks[name]
        is_ok, detail = run_oracle_on_files(t.reference_solution, t.task_dir)
        if is_ok is True:
            print(f"  OK   {name}")
            ok += 1
        elif is_ok is False:
            print(f"  FAIL {name} :: {detail[:80]}")
            fail += 1
        else:
            print(f"  ERR  {name} :: {detail[:80]}")
            err += 1

    print(f"\nSummary: {ok} passed, {fail} failed, {err} errors/unknown (n={len(names)})")
    sys.exit(0 if fail == 0 and err == 0 else 1)


if __name__ == "__main__":
    main()
