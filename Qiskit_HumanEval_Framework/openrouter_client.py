"""
OpenRouter API client (standalone copy; avoids depending on QHack generate_tests.py).
"""

from __future__ import annotations

import time
from typing import Optional

import requests

from config import (
    OPENROUTER_API_KEY,
    OPENROUTER_URL,
    MODELS,
    DEFAULT_MODEL,
    TEMPERATURE,
    MAX_RETRIES,
    RETRY_DELAY,
    MODEL_MAX_TOKENS,
    DEFAULT_MAX_TOKENS,
    MIN_RESPONSE_CHARS,
)

_DEFAULT_SYSTEM = "You are a helpful assistant."


def call_openrouter(
    prompt: str,
    model_key: str = DEFAULT_MODEL,
    temperature: float = TEMPERATURE,
    system_prompt: Optional[str] = None,
) -> Optional[str]:
    if not (OPENROUTER_API_KEY or "").strip():
        print(
            "Error: OPENROUTER_API_KEY is empty. Set the environment variable or "
            "create a .env file next to config.py (see .env.example)."
        )
        return None
    model_id = MODELS[model_key]
    max_tokens = MODEL_MAX_TOKENS.get(model_key, DEFAULT_MAX_TOKENS)
    sys_msg = system_prompt if system_prompt is not None else _DEFAULT_SYSTEM
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/qiskit-community/qiskit-human-eval",
        "X-Title": "Qiskit HumanEval evaluation framework",
    }
    payload = {
        "model": model_id,
        "messages": [
            {"role": "system", "content": sys_msg},
            {"role": "user", "content": prompt},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(
                f"        API call {attempt}/{MAX_RETRIES} [{model_id}] ...",
                end=" ",
                flush=True,
            )
            resp = requests.post(
                OPENROUTER_URL,
                headers=headers,
                json=payload,
                timeout=300,
            )
            resp.raise_for_status()
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            finish = data["choices"][0].get("finish_reason", "unknown")
            print(f"ok ({len(content)} chars, finish={finish})")

            if finish == "length":
                print(
                    f"        WARNING: response truncated; consider raising "
                    f"MODEL_MAX_TOKENS for '{model_key}'."
                )

            if len(content.strip()) < MIN_RESPONSE_CHARS:
                print(
                    f"        response too short ({len(content.strip())} chars) — retrying ..."
                )
                if attempt < MAX_RETRIES:
                    time.sleep(RETRY_DELAY)
                    continue
                print("        all retries returned short responses — skipping")
                return None

            return content

        except requests.exceptions.Timeout:
            print("timeout")
        except requests.exceptions.HTTPError as e:
            code = e.response.status_code
            print(f"HTTP {code}: {e.response.text[:120]}")
            if code in (400, 401, 403):
                return None
        except Exception as e:
            print(f"{e}")

        if attempt < MAX_RETRIES:
            print(f"        retrying in {RETRY_DELAY}s ...")
            time.sleep(RETRY_DELAY)

    return None
