"""
challenge_mapper.py
===================
Discovers and maps all 8 challenges, their human solutions, and their
LLM-generated solutions into structured data objects.

Key fixes vs previous version:
  1. Uses improved notebook_utils.extract_code_from_notebook which strips
     markdown code fences from papermill-failed notebooks.
  2. Calls inject_harness_if_missing() so that LLM solutions without
     run()/check() get the harness injected from the official template.
  3. Handles the gpt4.1/rainy_days_retreat misplaced files (they live in
     an /images/ subfolder instead of the challenge root).
"""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from config import (
    FRAMEWORK_ROOT,
    CHALLENGES_SUBDIR,
    HUMAN_SOLUTIONS_SUBDIR,
    LLM_SOLUTIONS_SUBDIR,
    CHALLENGE_NAMES,
    LLM_SOLUTION_MODELS,
    LLM_SOLUTION_VARIANTS,
    MAX_CODE_CHARS,
)
from notebook_utils import (
    extract_code_from_notebook,
    extract_code_from_py,
    load_solution_code,
    inject_harness_if_missing,
    parse_test_cases,
)


# ── DATA CLASSES ──────────────────────────────────────────────────────────────

@dataclass
class ChallengeInfo:
    name:           str
    template_path:  Path
    description:    str
    reference_code: str
    test_cases:     List[Tuple[str, str]]


@dataclass
class HumanSolution:
    challenge_name: str
    solution_set:   str
    path:           Path
    code:           str


@dataclass
class LLMSolution:
    challenge_name: str
    llm_model:      str
    variant:        str
    path:           Path
    code:           str
    harness_injected: bool = False   # True if run()/check() were injected


# ── TITLE → CHALLENGE KEYWORD MAP ─────────────────────────────────────────────

_TITLE_MAP: Dict[str, str] = {
    "chalet":          "chalet_random_gate",
    "random_gate":     "chalet_random_gate",
    "random gate":     "chalet_random_gate",
    "the chalet":      "chalet_random_gate",
    "coffee":          "coffee_conundrum",
    "conundrum":       "coffee_conundrum",
    "contextuality":   "contextuality_dunes",
    "dunes":           "contextuality_dunes",
    "context":         "contextuality_dunes",
    "mach":            "mach_zender_cabin",
    "zender":          "mach_zender_cabin",
    "mach-zender":     "mach_zender_cabin",
    "cabin":           "mach_zender_cabin",
    "qsp":             "QSP_swamp",
    "swamp":           "QSP_swamp",
    "rainy":           "rainy_days_retreat",
    "retreat":         "rainy_days_retreat",
    "forest":          "rainy_days_retreat",
    "eigentracks":     "travelling_eigentracks",
    "travelling":      "travelling_eigentracks",
    "traveling":       "travelling_eigentracks",
    "triple":          "triple_H_hotel",
    "hotel":           "triple_H_hotel",
    "triple h":        "triple_H_hotel",
    "triple_h":        "triple_H_hotel",
}


def _canonical_name(raw: str) -> Optional[str]:
    """Try to map a filename / folder name to a canonical challenge name."""
    raw_lower = raw.lower().replace("-", "_").replace(" ", "_")
    for cname in CHALLENGE_NAMES:
        if cname.lower() == raw_lower:
            return cname
    for cname in CHALLENGE_NAMES:
        if cname.lower() in raw_lower or raw_lower in cname.lower():
            return cname
    raw_space = raw.lower().replace("_", " ").replace("-", " ")
    for kw, cname in _TITLE_MAP.items():
        if kw in raw_space:
            return cname
    return None


# ── MAIN MAPPER ───────────────────────────────────────────────────────────────

class ChallengeMapper:

    def __init__(self, framework_root: Optional[str] = None):
        self.root          = Path(framework_root or FRAMEWORK_ROOT)
        self.challenges_dir = self.root / CHALLENGES_SUBDIR
        self.human_sol_dir  = self.root / HUMAN_SOLUTIONS_SUBDIR
        self.llm_sol_dir    = self.root / LLM_SOLUTIONS_SUBDIR

    # ── CHALLENGES ────────────────────────────────────────────────────────────

    def load_challenges(self) -> Dict[str, ChallengeInfo]:
        result: Dict[str, ChallengeInfo] = {}
        for name in CHALLENGE_NAMES:
            ch_dir = self.challenges_dir / name
            if not ch_dir.exists():
                print("  WARNING: challenge directory not found: {}".format(ch_dir))
                continue

            template = ch_dir / "template.ipynb"
            if not template.exists():
                print("  WARNING: template.ipynb missing for {}".format(name))
                continue

            desc_path = ch_dir / "description.md"
            description = (
                desc_path.read_text(encoding="utf-8", errors="replace")
                if desc_path.exists() else ""
            )

            reference_code = extract_code_from_notebook(template, MAX_CODE_CHARS)
            test_cases     = parse_test_cases(reference_code)

            result[name] = ChallengeInfo(
                name=name,
                template_path=template,
                description=description[:800],
                reference_code=reference_code,
                test_cases=test_cases,
            )

        print("  Loaded {}/8 challenges.".format(len(result)))
        return result

    # ── HUMAN SOLUTIONS ───────────────────────────────────────────────────────

    def load_human_solutions(self) -> Dict[str, List[HumanSolution]]:
        result: Dict[str, List[HumanSolution]] = {n: [] for n in CHALLENGE_NAMES}

        if not self.human_sol_dir.exists():
            print("  WARNING: human solutions directory not found: {}".format(
                self.human_sol_dir))
            return result

        for sol_set_dir in sorted(self.human_sol_dir.iterdir()):
            if not sol_set_dir.is_dir() or sol_set_dir.name.startswith("__"):
                continue
            sol_set = sol_set_dir.name

            for fpath in sorted(sol_set_dir.iterdir()):
                if fpath.suffix not in (".ipynb", ".py"):
                    continue
                if fpath.name.startswith("._"):
                    continue

                cname = _canonical_name(fpath.stem)
                if cname is None:
                    print("  WARNING: cannot map '{}' to a challenge".format(fpath.name))
                    continue

                try:
                    code = load_solution_code(fpath, MAX_CODE_CHARS)
                    if not code.strip():
                        continue
                    result[cname].append(HumanSolution(
                        challenge_name=cname,
                        solution_set=sol_set,
                        path=fpath,
                        code=code,
                    ))
                except Exception as e:
                    print("  WARNING: could not load {}: {}".format(fpath, e))

        totals = {n: len(v) for n, v in result.items()}
        print("  Human solutions loaded: {}".format(totals))
        return result

    # ── LLM SOLUTIONS ─────────────────────────────────────────────────────────

    def load_llm_solutions(
        self,
        llm_models: Optional[List[str]] = None,
        variants:   Optional[List[str]] = None,
    ) -> Dict[str, Dict[str, List[LLMSolution]]]:
        """
        Returns nested dict: {challenge_name: {llm_model: [LLMSolution, ...]}}

        Fixes applied:
          - Strips markdown fences from papermill-failed notebooks
          - Injects run()/check() harness when missing
          - Searches subdirectories for misplaced files (gpt4.1/rainy_days)
        """
        llm_models = llm_models or LLM_SOLUTION_MODELS
        variants   = variants   or LLM_SOLUTION_VARIANTS

        result: Dict[str, Dict[str, List[LLMSolution]]] = {
            n: {m: [] for m in llm_models} for n in CHALLENGE_NAMES
        }

        if not self.llm_sol_dir.exists():
            print("  WARNING: LLM solutions directory not found: {}".format(
                self.llm_sol_dir))
            return result

        for llm_model in llm_models:
            llm_dir = self.llm_sol_dir / llm_model
            if not llm_dir.exists():
                print("  WARNING: LLM model folder not found: {}".format(llm_dir))
                continue

            for ch_dir in sorted(llm_dir.iterdir()):
                if not ch_dir.is_dir():
                    continue

                cname = _canonical_name(ch_dir.name)
                if cname is None:
                    print("  WARNING: cannot map '{}' to a challenge".format(ch_dir.name))
                    continue

                # Template path for harness injection
                template_path = (self.challenges_dir / cname / "template.ipynb")

                for variant in variants:
                    # Search in ch_dir and all immediate subdirs
                    # (fixes gpt4.1/rainy_days where files are in /images/)
                    candidate_paths = [ch_dir] + [
                        d for d in ch_dir.iterdir() if d.is_dir()
                    ]
                    found = False
                    for search_dir in candidate_paths:
                        fpath = search_dir / "{}.ipynb".format(variant)
                        if fpath.exists():
                            try:
                                code = extract_code_from_notebook(fpath, MAX_CODE_CHARS)
                                if not code.strip():
                                    continue

                                # Inject harness if run()/check() are missing
                                original_code = code
                                code = inject_harness_if_missing(code, template_path)
                                harness_injected = (code != original_code)

                                result[cname][llm_model].append(LLMSolution(
                                    challenge_name=cname,
                                    llm_model=llm_model,
                                    variant=variant,
                                    path=fpath,
                                    code=code,
                                    harness_injected=harness_injected,
                                ))
                                found = True
                                break
                            except Exception as e:
                                print("  WARNING: could not load {}: {}".format(fpath, e))

        totals = {n: {m: len(v) for m, v in mv.items()} for n, mv in result.items()}
        print("  LLM solutions loaded (challenge x model counts):")
        for cname, mv in totals.items():
            injected = sum(
                1 for m in llm_models
                for s in result[cname].get(m, [])
                if s.harness_injected
            )
            inj_str = " ({} harness-injected)".format(injected) if injected else ""
            print("    {}: {}{}".format(cname, mv, inj_str))

        return result
