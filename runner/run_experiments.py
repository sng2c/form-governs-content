"""Assemble prompts from (content x form) and run the experiment.

Each cell = (content_item, form) is run n_repeats times with varied seeds.
Results are written to data/raw_runs.jsonl.

Usage:
    python -m runner.run_experiments
    python -m runner.run_experiments --dry-run
"""
import argparse
import json
import time
from pathlib import Path

from .forms import load_forms, family
from .llm import chat, load_config

CONTENT_PATH = Path(__file__).resolve().parent.parent / "content" / "dataset.json"
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
OUT_PATH = DATA_DIR / "raw_runs.jsonl"


def build_prompt(content: dict, form_template: str) -> str:
    facts = "\n".join(f"- {f}" for f in content["neutral_facts"])
    return form_template.format(facts=facts, question=content["contested_question"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="build prompts but don't call the model")
    ap.add_argument("--out", default=str(OUT_PATH))
    args = ap.parse_args()

    config = load_config()
    forms = load_forms()
    contents = json.loads(CONTENT_PATH.read_text())
    contents_by_id = {c["id"]: c for c in contents}

    selected_forms = config["forms"]
    selected_items = config["content_items"]
    n_repeats = config["n_repeats"]
    seed_base = config["seed"]

    DATA_DIR.mkdir(exist_ok=True)

    cells = []
    for cid in selected_items:
        c = contents_by_id[cid]
        for fname in selected_forms:
            cells.append((c, fname))

    print(f"Cells: {len(cells)}  | repeats/cell: {n_repeats}  | total calls: {len(cells)*n_repeats}")

    with open(args.out, "w", buffering=1) as f:  # line-buffered so progress is visible
        for ci, (content, fname) in enumerate(cells):
            prompt = build_prompt(content, forms[fname])
            if args.dry_run:
                record = {
                    "content_id": content["id"],
                    "form": fname,
                    "family": family(fname),
                    "repeat_idx": 0,
                    "prompt": prompt,
                    "response": "[dry-run]",
                    "seed": seed_base,
                }
                f.write(json.dumps(record) + "\n")
                continue

            t0 = time.time()
            responses = chat(prompt, config, seed=seed_base, n=n_repeats)
            dt = time.time() - t0
            for ri, resp in enumerate(responses):
                record = {
                    "content_id": content["id"],
                    "domain": content["domain"],
                    "form": fname,
                    "family": family(fname),
                    "repeat_idx": ri,
                    "seed": seed_base + ri,
                    "prompt": prompt,
                    "response": resp,
                }
                f.write(json.dumps(record) + "\n")
            f.flush()
            print(f"[{ci+1}/{len(cells)}] {content['id']} x {fname}: {n_repeats} runs in {dt:.1f}s", flush=True)
            time.sleep(0.2)

    print(f"Wrote {args.out}", flush=True)


if __name__ == "__main__":
    main()