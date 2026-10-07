"""
notebook_utils.py
=================
Utilities for extracting Python code from Jupyter notebooks (.ipynb)
and plain .py files.

Key fixes vs previous version:
  1. Strip markdown code fences (```python ... ```) that appear inside code
     cells in papermill-failed notebooks — these were causing load_error for
     ~20 of the 64 LLM solutions.
  2. Inject run() / check() harness from the official template when a solution
     is missing it — fixes the 9 solutions (qwen3 RAG, gpt4.1 rag variants)
     that have the main function but no test harness.
  3. Robust test_cases extraction using a bracket-depth parser (handles
     multi-line lists that the old regex missed).
"""

import json
import re
from pathlib import Path
from typing import List, Optional, Tuple


# ── CODE EXTRACTION ───────────────────────────────────────────────────────────

def extract_code_from_notebook(path: Path, max_chars: int = 0) -> str:
    """
    Join all code cells of a notebook into a single Python string.

    Handles:
    - Normal code cells
    - Papermill-failed notebooks where code is wrapped in ```python fences
      inside code cells (the fence is stripped automatically)
    - Cells with mixed fence + raw code content

    If max_chars > 0, truncate the result to that many characters.
    """
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        nb = json.load(f)

    parts = []
    for cell in nb.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        src = cell.get("source", [])
        text = "".join(src) if isinstance(src, list) else src
        if not text.strip():
            continue
        cleaned = _strip_code_fences(text)
        if cleaned.strip():
            parts.append(cleaned)

    code = "\n\n".join(parts)
    if max_chars and len(code) > max_chars:
        code = code[:max_chars]
    return code


def _strip_code_fences(text: str) -> str:
    """
    Remove ```python / ``` fences from text that appears inside a code cell.
    This happens in papermill-failed notebooks where the LLM output was stored
    as a literal markdown code block inside a code cell.
    """
    # Pattern: ```python\n...``` or ```\n...```
    cleaned = re.sub(r"```(?:python)?\n", "", text)
    cleaned = re.sub(r"```\s*$", "", cleaned, flags=re.MULTILINE)
    return cleaned.strip()


def extract_code_from_py(path: Path, max_chars: int = 0) -> str:
    """Read a plain .py file and return its contents."""
    text = path.read_text(encoding="utf-8", errors="replace")
    if max_chars and len(text) > max_chars:
        text = text[:max_chars]
    return text


def load_solution_code(path: Path, max_chars: int = 0) -> str:
    """Auto-detect .ipynb vs .py and extract code accordingly."""
    if path.suffix == ".ipynb":
        return extract_code_from_notebook(path, max_chars)
    elif path.suffix == ".py":
        return extract_code_from_py(path, max_chars)
    else:
        raise ValueError("Unsupported file type: {}".format(path.suffix))


# ── HARNESS INJECTION ─────────────────────────────────────────────────────────

def extract_template_harness(template_path: Path) -> Tuple[Optional[str], Optional[str]]:
    """
    Extract the run() and check() functions from the official challenge template.
    Returns (run_code, check_code) — either may be None if not found.
    """
    code = extract_code_from_notebook(template_path)

    run_code   = _extract_function(code, "run")
    check_code = _extract_function(code, "check")
    return run_code, check_code


def _extract_function(code: str, func_name: str) -> Optional[str]:
    """
    Extract a complete function definition from a code string.
    Uses indentation to determine where the function ends.
    """
    pattern = r"(^def {}\s*\(.*?)(?=^def |\Z)".format(re.escape(func_name))
    m = re.search(pattern, code, re.M | re.DOTALL)
    if m:
        return m.group(1).rstrip()
    return None


def inject_harness_if_missing(
    solution_code: str,
    template_path: Path,
) -> str:
    """
    If solution_code is missing run() or check(), inject them from the
    official template. This fixes qwen3 RAG solutions and gpt4.1 RAG
    variants that only have the main function without the test harness.

    Returns the (possibly augmented) solution code.
    """
    has_run   = bool(re.search(r"^def run\s*\(", solution_code, re.M))
    has_check = bool(re.search(r"^def check\s*\(", solution_code, re.M))

    if has_run and has_check:
        return solution_code  # nothing to do

    if not template_path.exists():
        return solution_code  # can't inject without template

    run_code, check_code = extract_template_harness(template_path)
    additions = []

    if not has_run and run_code:
        additions.append(run_code)
    if not has_check and check_code:
        additions.append(check_code)

    if additions:
        # Also inject the test_cases list if missing
        has_test_cases = "test_cases" in solution_code
        if not has_test_cases:
            template_code = extract_code_from_notebook(template_path)
            tc = parse_test_cases(template_code)
            if tc:
                tc_str = "test_cases = [\n"
                for inp, exp in tc:
                    tc_str += "    ({!r}, {!r}),\n".format(inp, exp)
                tc_str += "]\n"
                additions.append(tc_str)

        return solution_code + "\n\n# --- harness injected from template ---\n" + "\n\n".join(additions)

    return solution_code


# ── TEST CASES EXTRACTION ─────────────────────────────────────────────────────

def parse_test_cases(code: str) -> List[Tuple[str, str]]:
    """
    Parse the test_cases = [...] list from challenge code.
    Uses a bracket-depth parser to handle multi-line lists.
    Returns list of (input_str, expected_str) tuples.
    """
    m = re.search(r"test_cases\s*=\s*\[", code)
    if not m:
        return []

    start = m.end() - 1  # position of opening '['
    depth = 0
    end   = start
    for i, ch in enumerate(code[start:], start):
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                end = i + 1
                break

    raw = code[start:end]
    try:
        cases = eval(raw)  # noqa: S307 — controlled, read-only source
        if isinstance(cases, list) and all(
            isinstance(c, (list, tuple)) and len(c) == 2 for c in cases
        ):
            return [(str(a), str(b)) for a, b in cases]
    except Exception:
        pass
    return []


def extract_test_cases_from_notebook(path: Path) -> List[Tuple[str, str]]:
    """Extract test_cases from a notebook file."""
    code = extract_code_from_notebook(path)
    return parse_test_cases(code)


# ── SYNTAX CHECK ──────────────────────────────────────────────────────────────

def check_syntax(code: str) -> Tuple[bool, str]:
    """Return (is_valid: bool, error_msg: str)."""
    import ast
    try:
        ast.parse(code)
        return True, ""
    except SyntaxError as e:
        return False, "SyntaxError line {}: {}".format(e.lineno, e.msg)


def strip_markdown_fences(text: str) -> str:
    """
    Remove ```python / ``` fences from LLM API responses and strip
    leading prose before the first import/def/# line.
    Also replaces non-ASCII characters with underscores.
    """
    text = re.sub(r"```(?:python)?\s*\n", "", text)
    text = re.sub(r"```\s*", "", text)
    lines = text.split("\n")
    start = 0
    for i, line in enumerate(lines):
        s = line.strip()
        if (s.startswith("import ")
                or s.startswith("from ")
                or s.startswith("def test_")
                or s.startswith("#")):
            start = i
            break
    code = "\n".join(lines[start:]).strip()
    code = code.encode("ascii", errors="replace").decode("ascii").replace("?", "_")
    return code
