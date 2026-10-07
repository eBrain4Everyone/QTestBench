"""
Shared layout and helpers for the Qiskit HumanEval benchmark (isolated from
Framework_Eight_Challenges / PennyLane QHack).

Paper: arXiv:2406.14712 — dataset follows HumanEval-style ``check(candidate)``.
"""

from __future__ import annotations

import ast
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Default bundle layout (sibling to this file)
_BUNDLE_DIR = Path(__file__).resolve().parent
QISKIT_HE_FRAMEWORK_ROOT = _BUNDLE_DIR / "Framework_Qiskit_Human_Eval"

TASKS_SUBDIR = "tasks"
GENERATED_TESTS_SUBDIR = "generated_tests"
HUMAN_SOLUTIONS_SUBDIR = "Human_solutions"
LLM_SOLUTIONS_SUBDIR = "LLM_generated_solutions"
CHECKPOINT_FILE_TEMPLATE = "generation_checkpoint_qiskit_he_{model}.json"

# Fixed task set for research runs (e.g. 10 stratified tasks): one ``task_NNNN`` per line.
SCOPE_TASKS_FILENAME = "evaluation_scope_tasks.txt"

# Folder names under LLM_generated_solutions/ that actually exist on disk.
# The Config 2 cohort is the union of these models' solutions per task, each
# oracle-labeled correct/wrong/unknown. Using all available models (not just one)
# is what gives the cohort both correct AND oracle-wrong probes, so CS, BDS and
# TQS are all well-defined.
LLM_SOLUTION_MODELS = ["claudeopus46", "deepseekv32", "gemini3pro", "gpt54", "qwen3"]
# Default stems; mapper also auto-loads any ``generated_*.py`` present per task.
LLM_SOLUTION_VARIANTS = [
    "generated_non_rag_1",
    "generated_non_rag_2",
    "generated_non_rag_3",
    "generated_rag_1",
]
# Target independent LLM attempts per model×task when enriching Config~2 cohort.
COHORT_SAMPLES_PER_TASK = 3


@dataclass
class QiskitHETask:
    """One row from the JSON, materialized as a task folder."""

    name: str
    task_id: str
    entry_point: str
    prompt: str
    reference_solution: str
    official_check: str
    difficulty_scale: str
    task_dir: Path
    # How reference_solution was assembled (see reference_solution_from_dataset_row).
    solution_format: str = ""

    @property
    def template_path(self) -> Optional[Path]:
        """Unused for Qiskit HE (no QHack template.ipynb); kept for API parity."""
        return None


def difficulty_bucket(difficulty_scale: str) -> str:
    """
    Map dataset ``difficulty_scale`` to sampling buckets.
    JSON uses ``basic``, ``intermediate``, ``difficult`` (paper / repo).
    """
    s = (difficulty_scale or "").strip().lower()
    if s == "basic":
        return "easy"
    if s == "intermediate":
        return "intermediate"
    if s in ("difficult", "hard"):
        return "hard"
    return "unknown"


def stratified_pick_tasks(
    pending: List[QiskitHETask],
    n_easy: int,
    n_intermediate: int,
    n_hard: int,
    n_any: int,
) -> Tuple[List[QiskitHETask], List[str]]:
    """
    Deterministic: sort by ``task_*`` name, take up to *n_easy* / *n_intermediate*
    / *n_hard* from each bucket, then add *n_any* further tasks from the remaining
    pending list in order (any difficulty). Unknown labels are only eligible for
    the ``any`` slots and for filling after bucket quotas.
    """
    warn: List[str] = []
    ordered = sorted(pending, key=lambda t: t.name)
    easy_l: List[QiskitHETask] = []
    mid_l: List[QiskitHETask] = []
    hard_l: List[QiskitHETask] = []
    unk_l: List[QiskitHETask] = []

    for t in ordered:
        b = difficulty_bucket(t.difficulty_scale)
        if b == "easy":
            easy_l.append(t)
        elif b == "intermediate":
            mid_l.append(t)
        elif b == "hard":
            hard_l.append(t)
        else:
            unk_l.append(t)

    def _take(src: List[QiskitHETask], want: int, label: str) -> List[QiskitHETask]:
        if want <= 0:
            return []
        got = src[:want]
        if len(got) < want:
            warn.append(
                "stratify: only {} of {} requested {} tasks (pending pool short)".format(
                    len(got), want, label
                )
            )
        return got

    selected: List[QiskitHETask] = []
    names = set()

    for t in _take(easy_l, n_easy, "easy (basic)"):
        selected.append(t)
        names.add(t.name)
    for t in _take(mid_l, n_intermediate, "intermediate"):
        selected.append(t)
        names.add(t.name)
    for t in _take(hard_l, n_hard, "hard (difficult)"):
        selected.append(t)
        names.add(t.name)

    rest = [t for t in ordered if t.name not in names]
    any_got = 0
    for t in rest:
        if any_got >= n_any:
            break
        selected.append(t)
        names.add(t.name)
        any_got += 1
    if n_any > 0 and any_got < n_any:
        warn.append(
            "stratify: only {} of {} 'any' tasks added (not enough pending)".format(
                any_got, n_any
            )
        )

    return selected, warn


def pending_bucket_counts(pending: List[QiskitHETask]) -> Dict[str, int]:
    c = {"easy": 0, "intermediate": 0, "hard": 0, "unknown": 0}
    for t in pending:
        b = difficulty_bucket(t.difficulty_scale)
        if b == "unknown":
            c["unknown"] += 1
        else:
            c[b] += 1
    return c


def normalize_official_test(test_src: str) -> str:
    """
    Human-eval *hard* JSON appends ``check(entry_point_fn)`` to self-test the
    reference. Strip that so we only ``exec`` a ``check`` definition and call
    ``check(candidate)`` with the solution under evaluation.
    """
    s = test_src.strip()
    s = re.sub(
        r"\n\s*check\s*\(\s*[A-Za-z_][A-Za-z0-9_]*\s*\)\s*\Z",
        "",
        s,
        flags=re.MULTILINE,
    )
    return s.rstrip() + "\n"


def build_full_solution(prompt: str, canonical_body: str) -> str:
    """
    *Full* dataset (dataset_qiskit_test_human_eval.json): ``prompt`` is imports +
    function stub + docstring; ``canonical_solution`` is **only the function body**
    (indented statements). Concatenation yields one executable module — same pattern
    as classic HumanEval.
    """
    if not prompt.endswith("\n"):
        prompt = prompt + "\n"
    return prompt + canonical_body


def reference_solution_from_dataset_row(row: Dict[str, Any], variant: str) -> str:
    """
    Build the same reference string ``prepare_qiskit_human_eval.py`` writes to
    ``reference_solution.py`` / ``Human_solutions``.

    - **full**: ``prompt`` + ``canonical_solution`` (body-only in JSON).
    - **hard**: ``canonical_solution`` is already a full module (natural-language
      prompt in JSON is not pasted into the solution file).
    """
    if variant == "full":
        return build_full_solution(row["prompt"], row["canonical_solution"])
    return str(row["canonical_solution"]).rstrip() + "\n"


def reference_solution_format_label(variant: str) -> str:
    if variant == "full":
        return "prompt_plus_canonical_body"
    if variant == "hard":
        return "standalone_canonical_module"
    return "unknown"


def ast_module_defines_entry_point(src: str, entry_point: str) -> bool:
    """Static check: module-level ``def entry_point`` (or async) exists."""
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return False
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name == entry_point:
                return True
    return False


def sanity_check_reference_solution(src: str, entry_point: str) -> Tuple[bool, str]:
    """
    Parse-only validation (no Qiskit import). Use before/after materialize to ensure
    the stored file is a complete module shape, not a lone body fragment.
    """
    try:
        ast.parse(src)
    except SyntaxError as e:
        return False, "syntax_error: line {}: {}".format(e.lineno, e.msg)
    if not ast_module_defines_entry_point(src, entry_point):
        return False, "missing top-level def {!r} (wrong fragment?)".format(entry_point)
    return True, "ok"


_OFFICIAL_START = "# --- Official check block start (injected) ---"
_OFFICIAL_END = "# --- Official check block end ---"


def official_check_injected_block(entry_point: str, official_check: str) -> str:
    """
    Prepended to each generated test file (like TEST_CASES on QHack).
    Evaluate strips lines between start/end markers before coverage metrics.
    """
    lines = [
        _OFFICIAL_START,
        "OFFICIAL_CHECK_SOURCE = {}".format(repr(official_check)),
        "ENTRY_POINT_NAME = {!r}".format(entry_point),
        _OFFICIAL_END,
        "",
    ]
    return "\n".join(lines)


def strip_injected_official_check_block(src: str) -> str:
    s = src
    while True:
        a = s.find(_OFFICIAL_START)
        if a < 0:
            break
        b = s.find(_OFFICIAL_END, a)
        if b < 0:
            break
        b = s.find("\n", b)
        if b < 0:
            s = s[:a]
            break
        s = s[:a] + s[b + 1 :]
    return s.lstrip("\n")


def official_strings_for_coverage(official_check: str) -> List[Tuple[str, str]]:
    """
    Build pseudo (input, expected) pairs for C_in-style metrics: string literals
    from the official ``check`` (same trick as matching official case strings).
    """
    literals: List[str] = []
    try:
        tree = ast.parse(official_check)
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                if len(node.value) >= 2:
                    literals.append(node.value)
    except SyntaxError:
        pass
    # de-dupe, preserve order
    seen = set()
    out: List[Tuple[str, str]] = []
    for s in literals:
        if s not in seen:
            seen.add(s)
            out.append((s, ""))
    return out


def load_tasks(framework_root: Path) -> Dict[str, QiskitHETask]:
    """
    Load all tasks under ``framework_root / TASKS_SUBDIR / task_*``.
    """
    root = Path(framework_root)
    tasks_dir = root / TASKS_SUBDIR
    result: Dict[str, QiskitHETask] = {}
    if not tasks_dir.is_dir():
        return result

    for d in sorted(tasks_dir.iterdir()):
        if not d.is_dir() or not d.name.startswith("task_"):
            continue
        meta_path = d / "metadata.json"
        if not meta_path.is_file():
            continue
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        ref_path = d / "reference_solution.py"
        chk_path = d / "official_check.py"
        pr_path = d / "prompt.txt"
        if not ref_path.is_file() or not chk_path.is_file():
            continue
        result[d.name] = QiskitHETask(
            name=d.name,
            task_id=meta.get("task_id", d.name),
            entry_point=meta["entry_point"],
            prompt=pr_path.read_text(encoding="utf-8") if pr_path.is_file() else "",
            reference_solution=ref_path.read_text(encoding="utf-8"),
            official_check=chk_path.read_text(encoding="utf-8"),
            difficulty_scale=meta.get("difficulty_scale", ""),
            task_dir=d,
            solution_format=meta.get("solution_format", ""),
        )
    return result


def load_evaluation_scope_tasks(
    framework_root: Path,
    scope_file: Optional[Path] = None,
) -> List[str]:
    """
    Read task folder names from a scope file: one ``task_NNNN`` per line.
    Lines starting with ``#`` and blank lines are ignored.
    """
    root = Path(framework_root)
    path = Path(scope_file) if scope_file is not None else root / SCOPE_TASKS_FILENAME
    if not path.is_file():
        return []
    out: List[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        if line.startswith("task_"):
            out.append(line)
    return out


def resolve_only_task_list(
    framework_root: Path,
    only_explicit: Optional[List[str]],
    only_file: Optional[Path],
    scoped: bool,
) -> Tuple[Optional[List[str]], str]:
    """
    Choose which ``task_*`` folders to process.

    Priority: ``--only`` > ``--only-file`` > ``--scoped`` (read scope file) > None (all tasks).

    Returns ``(only_list, note)`` where ``note`` is a short message for logging.
    """
    if only_explicit:
        return list(only_explicit), "explicit --only ({} tasks)".format(len(only_explicit))

    if only_file is not None:
        p = Path(only_file).expanduser()
        if not p.is_file():
            raise FileNotFoundError("scope file not found: {}".format(p))
        names = load_evaluation_scope_tasks(framework_root, p)
        if not names:
            raise ValueError("no task_* lines in {}".format(p))
        return names, "--only-file {} ({} tasks)".format(p, len(names))

    if scoped:
        root = Path(framework_root)
        p = root / SCOPE_TASKS_FILENAME
        names = load_evaluation_scope_tasks(root)
        if not names:
            raise FileNotFoundError(
                "--scoped requires {} under --root (create it with one task_* per line). "
                "See evaluation_scope_tasks.example.txt".format(SCOPE_TASKS_FILENAME)
            )
        return names, "--scoped {} ({} tasks)".format(p, len(names))

    return None, "all tasks in corpus"


def default_dataset_paths() -> Tuple[Path, Path]:
    """JSON datasets shipped next to this package under ``datasets/``."""
    base = _BUNDLE_DIR / "datasets"
    return (
        base / "dataset_qiskit_test_human_eval.json",
        base / "dataset_qiskit_test_human_eval_hard.json",
    )
