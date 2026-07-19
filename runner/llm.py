"""Thin Ollama-Cloud (OpenAI-compatible) chat client.

Uses endpoint + API key from config.json. The key is read from the env var named
in config["api_key_env"] (default OLLAMA_API_KEY).
"""
import json
import os
import time
from pathlib import Path

import requests

from dotenv import load_dotenv

CONFIG_PATH = Path(__file__).resolve().parent / "config.json"
ENV_PATH = Path(__file__).resolve().parent.parent / ".env"

# Load .env (OLLAMA_API_KEY, ...) at import time so any run picks it up.
load_dotenv(ENV_PATH)


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text())


def chat(prompt: str, config: dict, *, seed: int, n: int = 1) -> list[str]:
    """Send a single user prompt; return n completions (content strings only)."""
    return [m["content"] for m in chat_meta(prompt, config, seed=seed, n=n)]


def chat_meta(prompt: str, config: dict, *, seed: int, n: int = 1) -> list[dict]:
    """Like chat() but returns rich metadata per completion: content, finish_reason,
    usage, and had_reasoning. Used by the MVP multi-model study."""
    api_key = os.environ[config["api_key_env"]]
    if not api_key:
        raise RuntimeError(f"Missing API key: set {config['api_key_env']} in .env")
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    out = []
    for i in range(n):
        body = {
            "model": config["model"],
            "messages": [{"role": "user", "content": prompt}],
            "temperature": config.get("temperature", 0.3),
            "seed": seed + i,  # vary seed across repeats to get within-form variance
            "max_tokens": config.get("max_tokens", 1024),
            "stream": False,
        }
        resp = _call_with_retry(config["endpoint"], headers, body)
        data = resp.json()
        msg = data["choices"][0]["message"]
        content = msg.get("content") or ""
        reasoning = msg.get("reasoning") or ""
        had_reasoning = bool(reasoning.strip())
        # Reasoning models (e.g. gpt-oss) put thinking in a separate field; keep
        # the final content, falling back to reasoning if content is empty.
        if not content.strip():
            content = reasoning
        out.append({
            "content": content,
            "finish_reason": data["choices"][0].get("finish_reason"),
            "usage": data.get("usage", {}),
            "had_reasoning": had_reasoning,
        })
    return out


def _call_with_retry(url, headers, body, *, retries: int = 4, base_timeout: int = 300):
    last = None
    for attempt in range(retries):
        try:
            r = requests.post(url, headers=headers, json=body, timeout=base_timeout)
            if r.status_code in (429, 500, 502, 503, 504):
                last = f"HTTP {r.status_code}: {r.text[:200]}"
                time.sleep(2 ** attempt)
                continue
            r.raise_for_status()
            return r
        except requests.RequestException as e:
            last = str(e)
            time.sleep(2 ** attempt)
    raise RuntimeError(f"LLM call failed after {retries} attempts: {last}")