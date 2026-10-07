"""
Updated configuration for the Eight‑Challenge QHack Framework.

This file centralises environment variables, model configuration and
directory layout used throughout the project.  Compared to the
original version shipped with the framework, the following changes
were made:

* Added support for newer large language models more suitable for
  code‑generation and quantum programming tasks in 2026.  The new
  models include:

    - **gpt54** — OpenAI’s GPT‑5.4, a successor to GPT‑4 with improved
      code generation capabilities【957044057431233†L45-L143】.
    - **gemini3pro** — Google’s Gemini 3.1 Pro model, noted for good
      price‑to‑performance and strong coding performance【957044057431233†L45-L143】.
    - **deepseekv32** — DeepSeek V3.2, a cost‑effective frontier model
      suitable for programming tasks【957044057431233†L45-L143】.
    - **claudeopus46** — Anthropic’s Claude Opus 4.6, which offers
      state‑of‑the‑art reasoning and coding abilities【957044057431233†L45-L143】.

  Older entries such as `gpt41` and `llama4` remain for backwards
  compatibility but are not selected by default.

* Updated the list of solution models under ``LLM_SOLUTION_MODELS`` so
  that evaluation probes recent high‑performing models by default.  You
  can override this list from the command line when running the
  evaluation script.

Other fields remain unchanged from the original configuration (API key
loading, directory paths, test generation defaults, etc.).
"""

import os


# ── API KEY ───────────────────────────────────────────────────────────────────

def _load_api_key() -> str:
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(env_path):
        with open(env_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if line.startswith("OPENROUTER_API_KEY="):
                    key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    if key:
                        return key
    raise EnvironmentError(
        "\n  OPENROUTER_API_KEY not found in .env file.\n"
        "  Create a .env file next to config.py containing:\n"
        "      OPENROUTER_API_KEY=sk-or-v1-your-key-here\n"
    )


def get_openrouter_api_key() -> str:
    """Return API key; raises if missing (for generation scripts)."""
    env_key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if env_key:
        return env_key
    return _load_api_key()


# Optional at import time so evaluate_solutions.py runs without .env.
try:
    OPENROUTER_API_KEY = get_openrouter_api_key()
except OSError:
    OPENROUTER_API_KEY = ""

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


# ── MODELS ────────────────────────────────────────────────────────────────────
#
# Mapping from short model keys to their OpenRouter identifiers.  See the
# module docstring above for an explanation of why these models were chosen.

MODELS = {
    # Legacy models (kept for backwards compatibility)
    "deepseek":   "deepseek/deepseek-r1",
    "gemini":     "google/gemini-2.5-flash-preview",
    "geminipro":  "google/gemini-2.5-pro-preview",
    "claude":     "anthropic/claude-opus-4-5",
    "deepseekv3": "deepseek/deepseek-v3.2",
    # GPT-4.1 family -> GPT-5.4 on OpenRouter (stronger code generation)
    "gpt41":      "openai/gpt-5.4",
    "gpt4.1":     "openai/gpt-5.4",
    "llama4":     "meta-llama/llama-4-maverick",
    # Same folder names as under LLM_generated_solutions/
    "llama-4":    "meta-llama/llama-4-maverick",

    # Newer code / quantum-friendly defaults (OpenRouter slugs)
    "gpt54":        "openai/gpt-5.4",
    # OpenRouter slug (not google/gemini-3.1-pro — that ID returns 400)
    "gemini3pro":   "google/gemini-3.1-pro-preview",
    "deepseekv32":  "deepseek/deepseek-v3.2",
    "claudeopus46": "anthropic/claude-opus-4-6",
    "qwen3":        "qwen/qwen3-coder-next",
    "llama33":      "meta-llama/llama-3.3-70b-instruct",
}

# Default model used when no model is specified.  You can change this to
# select your preferred test‑generation model; here we default to the
# latest cost‑effective DeepSeek variant.
DEFAULT_MODEL = "deepseekv32"


# Maximum token limits per model.  These values are estimates based on
# publicly available information.  Adjust them if your API provider
# enforces different quotas.
MODEL_MAX_TOKENS = {
    "deepseek":    8192,
    "gemini":      4096,
    "geminipro":   32000,
    "claude":      8192,
    "deepseekv3":  8192,
    "gpt41":       32768,
    "gpt4.1":      32768,
    "llama4":      8192,
    "llama-4":     8192,
    "gpt54":       32768,
    "gemini3pro":  32768,
    "deepseekv32": 8192,
    "claudeopus46":8192,
    "qwen3":       32768,
    "llama33":     16384,
}

DEFAULT_MAX_TOKENS = 4096

MIN_RESPONSE_CHARS = 200


# ── DIRECTORY LAYOUT ──────────────────────────────────────────────────────────

# Root of the framework.  By default this is the ``Framework_Eight_Challenges``
# folder co‑located with this configuration file.  You can override this
# when running the scripts via the ``--root`` CLI argument.
FRAMEWORK_ROOT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "Framework_Eight_Challenges"
)

CHALLENGES_SUBDIR        = "Challenges"
HUMAN_SOLUTIONS_SUBDIR   = "Human_solutions"
LLM_SOLUTIONS_SUBDIR     = "LLM_generated_solutions"
GENERATED_TESTS_SUBDIR   = "generated_tests"
CHECKPOINT_FILE_TEMPLATE = "generation_checkpoint_{model}.json"


# ── 8 CANONICAL CHALLENGE NAMES ───────────────────────────────────────────────

CHALLENGE_NAMES = [
    "chalet_random_gate",
    "coffee_conundrum",
    "contextuality_dunes",
    "mach_zender_cabin",
    "QSP_swamp",
    "rainy_days_retreat",
    "travelling_eigentracks",
    "triple_H_hotel",
]

# LLM solution models whose notebooks live under LLM_generated_solutions/
#
# The default list now includes the 2026 models introduced above.  You can
# override this list at runtime via the ``--llm-models`` flag when running
# ``evaluate_solutions.py`` or ``run_pipeline.py``.
# Must match folder names under LLM_generated_solutions/
LLM_SOLUTION_MODELS   = ["gemini", "gpt4.1", "llama-4", "qwen3"]
LLM_SOLUTION_VARIANTS = ["generated_non_rag_1", "generated_rag_1"]


# ── GENERATION SETTINGS ───────────────────────────────────────────────────────

NUM_TESTS_PER_TYPE = 3
TEMPERATURE        = 0.8
# 0 = load full file (no truncation). Values like 3500 cut long ``.py`` human
# solutions mid-string and make ``exec``/``ast.parse`` fail with SyntaxError.
MAX_CODE_CHARS     = 0


# ── LIMIT ─────────────────────────────────────────────────────────────────────

DEFAULT_LIMIT = None


# ── RATE‑LIMITING ─────────────────────────────────────────────────────────────

MAX_RETRIES         = 3
RETRY_DELAY         = 5.0
DELAY_BETWEEN_CALLS = 1.5


# ── EVALUATION THRESHOLDS ─────────────────────────────────────────────────────

EVAL_ATOL = 1e-4