"""Analyze Exp 3 across models: does the triad's Aufhebung reproduce on small
NON-reasoning local models (not just the reasoning 12B)?

Groups by (model, item). For each model: marker rate, refuses-binary rate,
third-proposition keyword count, within-item novelty. Then compares reasoning
(gemma4:12b-mlx) vs non-reasoning (llama3.2:3b, gemma3:4b).

The KEY output is the human-J surface: the SYNTHESIS CONCLUSION line for each
(model, item), to judge whether each is a genuine third proposition — and whether
non-reasoning small models produce genuine syntheses too.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

import numpy as np

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
RAW_PATH = DATA_DIR / "exp3_runs.jsonl"
OUT_PATH = DATA_DIR / "exp3_analysis.json"

THIRD_WORDS = ["higher", "reframe", "instead", "not as", "but as", "elevat", "redefine",
               "transition", "third", "mediate", "refram", "sublat", "higher determination",
               "rather than", "transcend", "reconceive", "shift from", "category error",
               "redesign", "reconfigure"]


def extract_synthesis(text):
    m = re.search(r"SYNTHESIS CONCLUSION:\s*(.+)", text, re.I | re.S)
    return m.group(1).strip().strip('"').strip() if m else None


def refuses_binary(text):
    t = text.lower()
    bare_yes = bool(re.search(r"\byes\b", t)) and not re.search(r"\bno\b", t)
    bare_no = bool(re.search(r"\bno\b", t)) and not re.search(r"\byes\b", t)
    return not (bare_yes or bare_no)


def third_count(text):
    t = text.lower()
    return sum(1 for w in THIRD_WORDS if w in t)


def shingle(s, k=3):
    s = s.lower().split()
    return set(tuple(s[i:i + k]) for i in range(len(s) - k + 1)) if len(s) >= k else {tuple(s)}


def main():
    runs = [json.loads(l) for l in RAW_PATH.read_text().splitlines() if l.strip()]
    for r in runs:
        r["synthesis"] = extract_synthesis(r["response"]) or r["response"][:300]
        r["has_marker"] = bool(extract_synthesis(r["response"]))
        r["refuses_binary"] = refuses_binary(r["synthesis"])
        r["third_word_count"] = third_count(r["synthesis"])

    models = sorted({r["model"] for r in runs})
    # model kind
    def kind(m):
        rs = [r for r in runs if r["model"] == m]
        return "reasoning" if rs and rs[0]["had_reasoning"] else "non-reasoning"

    by_model_item = defaultdict(list)
    for r in runs:
        by_model_item[(r["model"], r["content_id"])].append(r)

    summary_by_model = {}
    for m in models:
        mrs = [r for r in runs if r["model"] == m]
        per_item = {}
        for cid in sorted({r["content_id"] for r in mrs}):
            rs = [r for r in mrs if r["content_id"] == cid]
            sh = [shingle(r["synthesis"]) for r in rs]
            dists = []
            for i in range(len(sh)):
                for j in range(i + 1, len(sh)):
                    u = sh[i] | sh[j]
                    if u:
                        dists.append(1 - len(sh[i] & sh[j]) / len(u))
            per_item[cid] = {
                "n": len(rs),
                "marker_rate": round(sum(r["has_marker"] for r in rs) / len(rs), 3),
                "refuses_binary_rate": round(sum(r["refuses_binary"] for r in rs) / len(rs), 3),
                "mean_third_word_count": round(np.mean([r["third_word_count"] for r in rs]), 2),
                "within_item_novelty": round(float(np.mean(dists)), 3) if dists else 0.0,
                "open_ended": rs[0]["is_open_ended"],
                "syntheses": [r["synthesis"][:220] for r in rs],
            }
        summary_by_model[m] = {
            "kind": kind(m),
            "n_runs": len(mrs),
            "mean_marker_rate": round(np.mean([v["marker_rate"] for v in per_item.values()]), 3),
            "mean_refuses_binary_rate": round(np.mean([v["refuses_binary_rate"] for v in per_item.values()]), 3),
            "mean_third_word_count": round(np.mean([v["mean_third_word_count"] for v in per_item.values()]), 2),
            "mean_within_item_novelty": round(np.mean([v["within_item_novelty"] for v in per_item.values()]), 3),
            "by_item": per_item,
        }

    out = {
        "n_runs": len(runs),
        "models": models,
        "by_model": summary_by_model,
    }
    OUT_PATH.write_text(json.dumps(out, indent=2, ensure_ascii=False))

    print(f"=== Exp 3 cross-model analysis ({len(runs)} runs) ===\n")
    print(f"{'model':>16} {'kind':>14} {'marker':>7} {'refuse':>7} {'third':>6} {'novelty':>7}")
    for m in models:
        s = summary_by_model[m]
        print(f"{m:>16} {s['kind']:>14} {s['mean_marker_rate']:>7} {s['mean_refuses_binary_rate']:>7} {s['mean_third_word_count']:>6} {s['mean_within_item_novelty']:>7}")

    print("\n--- Per-model syntheses (human-J: genuine THIRD proposition?) ---")
    for m in models:
        print(f"\n### {m} ({summary_by_model[m]['kind']})")
        for cid, v in summary_by_model[m]["by_item"].items():
            tag = "OPEN" if v["open_ended"] else "cont"
            print(f"  [{cid}] ({tag}) marker={v['marker_rate']} refuse={v['refuses_binary_rate']} third={v['mean_third_word_count']} novelty={v['within_item_novelty']}")
            for k, syn in enumerate(v["syntheses"]):
                print(f"     r{k}: {syn}")

    print(f"\nWrote {OUT_PATH}")


if __name__ == "__main__":
    main()