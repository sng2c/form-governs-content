"""Exp 3 — local verification that the dialectical triad's Aufhebung (creative
synthesis) is robust to model scale/type, incl. non-reasoning small models.

Runs ONLY the dialectical_triad form (the creative form) on local Ollama model(s),
across the existing contested items + 2 open-ended design items, n repeats. Supports
a list of models and an append mode so multiple models can be accumulated into one
data file for cross-model comparison.
"""
import argparse
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
    ap.add_argument("--append", action="store_true",
                    help="append to existing file instead of overwriting")
    ap.add_argument("--models", help="comma-separated override list of local models")
    args = ap.parse_args()

    cfg = json.loads(EXP3_CFG_PATH.read_text())
    base = {
        "endpoint": cfg["endpoint"],
        "api_key_env": cfg["api_key_env"],
        "temperature": cfg["temperature"],
        "max_tokens": cfg["max_tokens"],
    }
    models = (args.models.split(",") if args.models
              else cfg.get("models") or [cfg["model"]])

    forms = load_forms()
    form_template = forms[cfg["form"]]

    contents = {c["id"]: c for c in json.loads(CONTENT_PATH.read_text())}
    contents.update({c["id"]: c for c in json.loads(EXP3_CONTENT_PATH.read_text())})

    items = cfg["content_items"]
    n_repeats = cfg["n_repeats"]
    seed_base = cfg["seed"]

    cells = [(m, cid) for m in models for cid in items]
    total = len(cells) * n_repeats
    print(f"=== Exp 3: triad on LOCAL models {models} | {len(items)} items x {n_repeats} = {total} calls ===", flush=True)
    DATA_DIR.mkdir(exist_ok=True)

    mode = "a" if args.append else "w"
    if mode == "a":
        print(f"(appending to {args.out})", flush=True)

    done = 0
    with open(args.out, mode, buffering=1) as f:
        for (m, cid) in cells:
            content = contents[cid]
            prompt = build_prompt(content, form_template)
            cmodel = {**base, "model": m}
            t0 = time.time()
            try:
                metas = chat_meta(prompt, cmodel, seed=seed_base, n=n_repeats)
                dt = time.time() - t0
                for ri, meta in enumerate(metas):
                    rec = {
                        "model": m,
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
                print(f"  [{done}/{total}] {m:>14} | {cid:>16} | {n_repeats}r {dt:.1f}s | reasoning={metas[0]['had_reasoning']}", flush=True)
            except Exception as e:
                print(f"  [ERR] {m} | {cid}: {str(e)[:140]}", flush=True)
            time.sleep(0.1)

    print(f"\nWrote {args.out}", flush=True)


if __name__ == "__main__":
    main()