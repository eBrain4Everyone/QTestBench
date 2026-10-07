"""
Load human (canonical) and LLM solutions for Framework_Qiskit_Human_Eval.

Human:  Human_solutions/<set>/task_NNNN.py
LLM:    LLM_generated_solutions/<model>/task_NNNN/<variant>.py
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

from qiskit_he_common import (
    HUMAN_SOLUTIONS_SUBDIR,
    LLM_SOLUTIONS_SUBDIR,
    LLM_SOLUTION_MODELS,
    LLM_SOLUTION_VARIANTS,
    load_tasks,
)


@dataclass
class QiskitHEHumanSolution:
    task_name: str
    solution_set: str
    path: Path
    code: str


@dataclass
class QiskitHELLMSolution:
    task_name: str
    llm_model: str
    variant: str
    path: Path
    code: str


class QiskitHEMapper:
    def __init__(self, framework_root: Path):
        self.root = Path(framework_root)
        self.human_dir = self.root / HUMAN_SOLUTIONS_SUBDIR
        self.llm_dir = self.root / LLM_SOLUTIONS_SUBDIR

    def load_tasks(self):
        return load_tasks(self.root)

    def load_human_solutions(self) -> Dict[str, List[QiskitHEHumanSolution]]:
        task_names = set(self.load_tasks().keys())
        result: Dict[str, List[QiskitHEHumanSolution]] = {n: [] for n in task_names}

        if not self.human_dir.is_dir():
            return result

        for sol_set_dir in sorted(self.human_dir.iterdir()):
            if not sol_set_dir.is_dir() or sol_set_dir.name.startswith("__"):
                continue
            for fpath in sorted(sol_set_dir.glob("*.py")):
                stem = fpath.stem
                if stem not in task_names:
                    continue
                code = fpath.read_text(encoding="utf-8", errors="replace")
                if code.strip():
                    result[stem].append(
                        QiskitHEHumanSolution(
                            task_name=stem,
                            solution_set=sol_set_dir.name,
                            path=fpath,
                            code=code,
                        )
                    )
        return result

    def load_llm_solutions(
        self,
        llm_models: Optional[List[str]] = None,
        variants: Optional[List[str]] = None,
    ) -> Dict[str, Dict[str, List[QiskitHELLMSolution]]]:
        llm_models = llm_models or list(LLM_SOLUTION_MODELS)
        variants = variants or list(LLM_SOLUTION_VARIANTS)
        task_names = list(self.load_tasks().keys())

        result: Dict[str, Dict[str, List[QiskitHELLMSolution]]] = {
            n: {m: [] for m in llm_models} for n in task_names
        }

        if not self.llm_dir.is_dir():
            return result

        for model in llm_models:
            mdir = self.llm_dir / model
            if not mdir.is_dir():
                continue
            for task_dir in sorted(mdir.iterdir()):
                if not task_dir.is_dir():
                    continue
                tname = task_dir.name
                if tname not in result:
                    continue

                stems: set[str] = set(variants)
                for fpath in sorted(task_dir.glob("generated_*.py")):
                    stems.add(fpath.stem)

                for stem in sorted(stems):
                    fpath = task_dir / f"{stem}.py"
                    if not fpath.is_file():
                        continue
                    code = fpath.read_text(encoding="utf-8", errors="replace")
                    if code.strip():
                        result[tname][model].append(
                            QiskitHELLMSolution(
                                task_name=tname,
                                llm_model=model,
                                variant=stem,
                                path=fpath,
                                code=code,
                            )
                        )
        return result
