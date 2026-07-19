"""Exp 3 — local verification that the dialectical triad's Aufhebung (creative
synthesis) is robust to a small local model (gemma4:12b-mlx).

Runs ONLY the dialectical_triad form (the creative form) on the local Ollama model,
across the existing contested items + 2 open-ended design items, n repeats. Stores
metadata so analyze_exp3 can compute Aufhebung proxies and surface the actual
syntheses for human J (the key qualitative check: is it a genuine third proposition?).
"""
import argparse
import copy
import json
import time
from pathlib import Path

from .forms import load_forms
from .llm import chat_meta

EXP3_CFG_PATH = Path(__file__).resolve().parent / "exp3_config.json"
CONTENT_PATH = Path(__file__).resolve().parent.parent / "content" / "dataset.json"
EXP3_CONTENT_PATH = Path(__file__).resolve().parent.parent / "content" / "exp3_items.json"
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
OUT_PATH = DATA_DIR / "exp3_runs.jsonl"


def build_prompt(content, form_template):
    facts = "\n".join(f"- {f}" for f in content["neutral_facts"])
    return form_template.format(facts=facts, question=content["contested_question"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(OUT_PATH))
    args = ap.parse_args()

    cfg = json.loads(EXP3_CFG_PATH.read_text())
    base = {
        "endpoint": cfg["endpoint"],
        "api_key_env": cfg["api_key_env"],
        "model": cfg["model"],
        "temperature": cfg["temperature"],
        "max_tokens": cfg["max_tokens"],
    }

    forms = load_forms()
    form_template = forms[cfg["form"]]

    # existing 3 items + 2 open-ended
    contents = {c["id"]: c for c in json.loads(CONTENT_PATH.read_text())}
    contents.update({c["id"]: c for c in json.loads(EXP3_CONTENT_PATH.read_text())})

    items = cfg["content_items"]
    n_repeats = cfg["n_repeats"]
    seed_base = cfg["seed"]

    cells = [(cid,) for cid in items]
    total = len(cells) * n_repeats
    print(f"=== Exp 3: triad on LOCAL {cfg['model']} | {len(items)} items x {n_repeats} = {total} local calls ===", flush=True)
    DATA_DIR.mkdir(exist_ok=True)

    done = 0
    with open(args.out, "w", buffering=1) as f:
        for (cid,) in cells:
            content = contents[cid]
            prompt = build_prompt(content, form_template)
            t0 = time.time()
            try:
                metas = chat_meta(prompt, base, seed=seed_base, n=n_repeats)
                dt = time.time() - t0
                for ri, meta in enumerate(metas):
                    rec = {
                        "model": cfg["model"],
                        "form": cfg["form"],
                        "content_id": cid,
                        "domain": content["domain"],
                        "repeat_idx": ri,
                        "seed": seed_base + ri,
                        "prompt": prompt,
                        "response": meta["content"],
                        "finish_reason": meta["finish_reason"],
                        "had_reasoning": meta["had_reasoning"],
                        "completion_tokens": meta["usage"].get("completion_tokens"),
                        "total_tokens": meta["usage"].get("total_tokens"),
                        "elapsed_s": round(dt / n_repeats, 1),
                        "is_open_ended": content["domain"] == "open-ended design",
                    }
                    f.write(json.dumps(rec) + "\n")
                done += n_repeats
                print(f"  [{done}/{total}] {cid:>16} | {n_repeats}r {dt:.1f}s | reasoning={metas[0]['had_reasoning']}", flush=True)
            except Exception as e:
                print(f"  [ERR] {cid}: {str(e)[:140]}", flush=True)
            time.sleep(0.1)

    print(f"\nWrote {args.out}", flush=True)


if __name__ == "__main__":
    main()