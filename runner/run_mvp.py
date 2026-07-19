"""MVP run: purpose -> template (binding) -> run across multiple Ollama-Cloud models.

Implements the frozen MVP: a finite purpose taxonomy bound to a finite dialectical
template library, run on diverse model types via Ollama Cloud, with metadata captured
for later analysis. The non-linear node (truly-ideal template Phi) stays a black box;
here we only exercise the linear spine: classify(no-op, purpose is given) -> bind ->
run -> store.

Usage:
    python -m runner.run_mvp                # full matrix
    python -m runner.run_mvp --check-only   # just ping every model, report which respond
"""
import argparse
import copy
import json
import time
from pathlib import Path

from .forms import load_forms
from .llm import chat_meta, load_config

MVP_CONFIG_PATH = Path(__file__).resolve().parent / "mvp_config.json"
CONTENT_PATH = Path(__file__).resolve().parent.parent / "content" / "dataset.json"
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
OUT_PATH = DATA_DIR / "mvp_runs.jsonl"


def load_mvp_config() -> dict:
    return json.loads(MVP_CONFIG_PATH.read_text())


def build_prompt(content: dict, form_template: str) -> str:
    facts = "\n".join(f"- {f}" for f in content["neutral_facts"])
    return form_template.format(facts=facts, question=content["contested_question"])


def check_models(mvp_cfg, base_cfg):
    """Ping every model with a tiny prompt; return (ok, failed)."""
    ok, failed = [], []
    for m in mvp_cfg["models"]:
        cfg = copy.deepcopy(base_cfg)
        cfg["model"] = m
        cfg["max_tokens"] = 16
        try:
            metas = chat_meta("Reply with just: OK", cfg, seed=1, n=1)
            content = (metas[0]["content"] or "").strip()
            print(f"  [OK]   {m:>22}  -> {content[:40]!r}", flush=True)
            ok.append(m)
        except Exception as e:
            print(f"  [FAIL] {m:>22}  -> {str(e)[:80]}", flush=True)
            failed.append(m)
    return ok, failed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-only", action="store_true")
    ap.add_argument("--out", default=str(OUT_PATH))
    args = ap.parse_args()

    mvp = load_mvp_config()
    base_cfg = load_config()
    base_cfg["endpoint"] = mvp["endpoint"]
    base_cfg["temperature"] = mvp["temperature"]
    base_cfg["max_tokens"] = mvp["max_tokens"]
    base_cfg["api_key_env"] = mvp["api_key_env"]

    print("=== Model connectivity check ===", flush=True)
    ok_models, failed = check_models(mvp, base_cfg)
    print(f"\nOK: {len(ok_models)}  FAILED: {len(failed)} -> {failed}", flush=True)
    if args.check_only:
        return
    if not ok_models:
        print("No models responded; aborting.", flush=True)
        return

    forms = load_forms()
    contents = {c["id"]: c for c in json.loads(CONTENT_PATH.read_text())}
    binding = mvp["binding"]
    purposes = mvp["purposes"]
    items = mvp["content_items"]
    n_repeats = mvp["n_repeats"]
    seed_base = mvp["seed"]

    cells = []
    for m in ok_models:
        for p in purposes:
            tname = binding[p]
            for cid in items:
                cells.append((m, p, tname, contents[cid]))

    total = len(cells) * n_repeats
    print(f"\n=== MVP run: {len(cells)} cells x {n_repeats} repeats = {total} calls ===", flush=True)
    DATA_DIR.mkdir(exist_ok=True)

    done = 0
    with open(args.out, "w", buffering=1) as f:
        for m, p, tname, content in cells:
            prompt = build_prompt(content, forms[tname])
            cfg = copy.deepcopy(base_cfg)
            cfg["model"] = m
            t0 = time.time()
            try:
                metas = chat_meta(prompt, cfg, seed=seed_base, n=n_repeats)
                dt = time.time() - t0
                for ri, meta in enumerate(metas):
                    rec = {
                        "model": m,
                        "model_type": mvp.get("model_types", {}).get(m, "unknown"),
                        "purpose": p,
                        "form": tname,
                        "content_id": content["id"],
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
                    }
                    f.write(json.dumps(rec) + "\n")
                done += n_repeats
                print(f"  [{done}/{total}] {m:>22} | {p:>18} | {content['id']:>14} | {n_repeats}r {dt:.1f}s", flush=True)
            except Exception as e:
                print(f"  [ERR] {m} | {p} | {content['id']}: {str(e)[:120]}", flush=True)
            time.sleep(0.2)

    print(f"\nWrote {args.out}", flush=True)


if __name__ == "__main__":
    main()