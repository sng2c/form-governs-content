"""Analyze Exp 3: does the dialectical triad's Aufhebung hold on a small local model?

Proxies per item:
  - has_synthesis_marker: SYNTHESIS CONCLUSION present.
  - refuses_binary: not a bare yes/no.
  - is_third_proposition: the synthesis contains markers of a *new* determination
    (re-framing words: 'higher', 'reframe', 'instead', 'not as ... but as', 'elevat',
    'redefine', 'transition', 'third', 'mediate'). Proxy for Aufhebung quality.
  - within-item novelty: shingle diversity across repeats (creative variance).
  - length / reasoning.

The KEY output is the human-J surface: the extracted SYNTHESIS CONCLUSION line for
each item, for the human to judge whether it is a genuine third proposition.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
RAW_PATH = DATA_DIR / "exp3_runs.jsonl"
OUT_PATH = DATA_DIR / "exp3_analysis.json"

THIRD_WORDS = ["higher", "reframe", "instead", "not as", "but as", "elevat", "redefine",
               "transition", "third", "mediate", "refram", "sublat", "higher determination",
               "rather than", "transcend", "reconceive", "shift from"]


def extract_synthesis(text):
    m = re.search(r"SYNTHESIS CONCLUSION:\s*(.+)", text, re.I | re.S)
    if m:
        return m.group(1).strip().strip('"').strip()
    return None


def refuses_binary(text):
    t = text.lower()
    bare_yes = bool(re.search(r"\byes\b", t)) and not re.search(r"\bno\b", t)
    bare_no = bool(re.search(r"\bno\b", t)) and not re.search(r"\byes\b", t)
    return not (bare_yes or bare_no)


def is_third_proposition(text):
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
        r["third_word_count"] = is_third_proposition(r["synthesis"])

    by_item = defaultdict(list)
    for r in runs:
        by_item[r["content_id"]].append(r)

    summary = {}
    for cid, rs in by_item.items():
        marker_rate = sum(1 for r in rs if r["has_marker"]) / len(rs)
        refuse_rate = sum(1 for r in rs if r["refuses_binary"]) / len(rs)
        third = [r["third_word_count"] for r in rs]
        # within-item novelty: mean pairwise shingle Jaccard distance among syntheses
        sh = [shingle(r["synthesis"]) for r in rs]
        import numpy as np
        dists = []
        for i in range(len(sh)):
            for j in range(i + 1, len(sh)):
                u = sh[i] | sh[j]
                if u:
                    dists.append(1 - len(sh[i] & sh[j]) / len(u))
        novelty = round(float(np.mean(dists)), 3) if dists else 0.0
        summary[cid] = {
            "n": len(rs),
            "marker_rate": round(marker_rate, 3),
            "refuses_binary_rate": round(refuse_rate, 3),
            "mean_third_word_count": round(float(np.mean(third)), 2),
            "within_item_novelty": novelty,
            "open_ended": rs[0]["is_open_ended"],
            "syntheses": [r["synthesis"][:240] for r in rs],
        }

    overall = {
        "model": runs[0]["model"] if runs else "?",
        "n_runs": len(runs),
        "mean_marker_rate": round(sum(s["marker_rate"] for s in summary.values()) / len(summary), 3),
        "mean_refuses_binary_rate": round(sum(s["refuses_binary_rate"] for s in summary.values()) / len(summary), 3),
        "mean_third_word_count": round(sum(s["mean_third_word_count"] for s in summary.values()) / len(summary), 2),
        "mean_within_item_novelty": round(sum(s["within_item_novelty"] for s in summary.values()) / len(summary), 3),
    }
    out = {"overall": overall, "by_item": summary}
    OUT_PATH.write_text(json.dumps(out, indent=2, ensure_ascii=False))

    print(f"=== Exp 3 analysis ({overall['n_runs']} runs, {overall['model']}) ===\n")
    print(f"Overall: marker={overall['mean_marker_rate']}  refuses_binary={overall['mean_refuses_binary_rate']}  third_words={overall['mean_third_word_count']}  within_novelty={overall['mean_within_item_novelty']}\n")
    print("Per item (human-J: read the syntheses — is each a genuine THIRD proposition?):")
    for cid, s in summary.items():
        tag = "OPEN" if s["open_ended"] else "cont"
        print(f"\n  [{cid}] ({tag}) marker={s['marker_rate']} refuse_binary={s['refuses_binary_rate']} third={s['mean_third_word_count']} novelty={s['within_item_novelty']}")
        for k, syn in enumerate(s["syntheses"]):
            print(f"     r{k}: {syn}")
    print(f"\nWrote {OUT_PATH}")


if __name__ == "__main__":
    main()