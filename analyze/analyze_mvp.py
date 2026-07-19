"""Analyze the MVP multi-model run.

For each (model, purpose, content) we ask: did the model, under the bound template,
produce an output that *realizes the purpose*? We measure purpose-realization with
cheap structural proxies (since the true judge J is the human architect):

  - decide        (red_blue_debate) : marker "DEBATE CONCLUSION", a clear stance,
                                      stance agreement across models (does form still
                                      govern the verdict across model types?).
  - synthesize    (dialectical_triad): marker "SYNTHESIS CONCLUSION", refuses the binary
                                      (no bare yes/no), introduces a new proposition
                                      (novelty vs the union of other models' shingles).
  - surface_assumptions (socratic_dialogue): marker "DIALOGUE CONCLUSION",
                                      question count, assumption-term density.

Outputs data/mvp_analysis.json + a printed summary.
"""
import json
import re
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
RAW_PATH = DATA_DIR / "mvp_runs.jsonl"
OUT_PATH = DATA_DIR / "mvp_analysis.json"


def load_runs():
    return [json.loads(l) for l in RAW_PATH.read_text().splitlines() if l.strip()]


def has_marker(text, marker):
    return marker.lower() in text.lower()


def stance(text, content_id):
    """Generic yes/no/qualified stance proxy (works for decide on both items)."""
    t = text.lower()
    neg = any(w in t for w in ["no,", "not ", "oppose", "against", "keep dwarf",
                              "stays a dwarf", "remains a dwarf", "does not support",
                              "without", "should not"])
    pos = any(w in t for w in ["yes", "support", "favor", "reclassify", "reclassified",
                              "reinstate", "raise", "mandate", "proceed", "enforce",
                              "supports"])
    qual = any(w in t for w in ["qualified", "conditional", "only if", "gradual",
                                "calibrated", "with safeguards", "pending", "if revised",
                                "mixed"])
    if neg and not pos:
        return "no"
    if pos and not neg:
        return "yes"
    if qual:
        return "qualified"
    if pos:
        return "yes"
    return "qualified"


def refuses_binary(text):
    t = text.lower()
    if re.search(r"\byes\b", t) and not re.search(r"\bno\b", t):
        return False  # a bare yes
    return any(w in t for w in ["qualified", "calibrated", "both", "neither", "third",
                               "synthesis", "conditional", "revised", "dual", "indexed",
                               "multi-criterion", "middle"])


def shingle(s, k=3):
    s = s.lower().split()
    return set(tuple(s[i:i + k]) for i in range(len(s) - k + 1)) if len(s) >= k else {tuple(s)}


def question_count(text):
    return text.count("?") + len(re.findall(r"\nQ[:.]", text))


def assumption_density(text):
    t = text.lower()
    terms = ["assum", "premis", "presuppos", "taken for granted", "if we assume",
             "underlying", "unspoken", "implicit"]
    return sum(t.count(w) for w in terms)


def purpose_metrics(purpose, text, content_id):
    m = {}
    if purpose == "decide":
        m["has_verdict_marker"] = has_marker(text, "DEBATE CONCLUSION")
        m["stance"] = stance(text, content_id)
        m["len"] = len(text)
    elif purpose == "synthesize":
        m["has_synthesis_marker"] = has_marker(text, "SYNTHESIS CONCLUSION")
        m["refuses_binary"] = refuses_binary(text)
        m["len"] = len(text)
    elif purpose == "surface_assumptions":
        m["has_dialogue_marker"] = has_marker(text, "DIALOGUE CONCLUSION")
        m["question_count"] = question_count(text)
        m["assumption_density"] = assumption_density(text)
        m["len"] = len(text)
    return m


def main():
    runs = load_runs()
    for r in runs:
        r["metrics"] = purpose_metrics(r["purpose"], r["response"], r["content_id"])

    # realization rate: fraction of repeats where the required marker is present.
    by_model_purpose = defaultdict(list)
    for r in runs:
        key = (r["model"], r["model_type"], r["purpose"], r["content_id"])
        by_model_purpose[key].append(r)

    realization = {}
    for (model, mtype, purpose, cid), rs in by_model_purpose.items():
        if purpose == "decide":
            key = "has_verdict_marker"
        elif purpose == "synthesize":
            key = "has_synthesis_marker"
        else:
            key = "has_dialogue_marker"
        rate = sum(1 for r in rs if r["metrics"].get(key)) / len(rs)
        realization.setdefault(model, {"model_type": mtype})[f"{purpose}/{cid}/{key}"] = rate

    # per (model, purpose, content): aggregate metrics + stance distribution
    per_cell = {}
    cell_stance = defaultdict(Counter)
    for r in runs:
        k = (r["model"], r["purpose"], r["content_id"])
        per_cell.setdefault(k, []).append(r)
        if r["purpose"] == "decide":
            cell_stance[k][r["metrics"]["stance"]] += 1

    # cross-model stance agreement for decide (form still governing verdict?)
    decide_agreement = {}
    for (model, purpose, cid), cnt in sorted(cell_stance.items()):
        if purpose != "decide":
            continue
        decide_agreement.setdefault(cid, {})[model] = dict(cnt)

    # model-type aggregates
    type_realization = defaultdict(lambda: defaultdict(list))
    for model, d in realization.items():
        mt = d["model_type"]
        for k, v in d.items():
            if k == "model_type":
                continue
            pur = k.split("/")[0]
            type_realization[mt][pur].append(v)
    type_summary = {}
    for mt, d in type_realization.items():
        type_summary[mt] = {pur: round(sum(v) / len(v), 3) for pur, v in d.items()}

    # novelty for synthesize: per content, fraction of a model's conclusion shingles
    # not present in other models' union (proxy for "introduces a new proposition").
    synth_novelty = defaultdict(list)
    syn_by_item = defaultdict(lambda: defaultdict(list))
    for r in runs:
        if r["purpose"] == "synthesize":
            syn_by_item[r["content_id"]][r["model"]].append(r["response"])
    for cid, by_model in syn_by_item.items():
        for m, concl in by_model.items():
            others = set()
            for g, cs in by_model.items():
                if g == m:
                    continue
                for c in cs:
                    others |= shingle(c)
            for c in concl:
                sh = shingle(c)
                if sh:
                    synth_novelty[m].append(1 - len(sh & others) / len(sh))

    novelty_by_model = {m: round(sum(v) / len(v), 3) for m, v in synth_novelty.items()}

    # verbosity / reasoning presence by model
    verb = defaultdict(list)
    reason = defaultdict(list)
    for r in runs:
        verb[r["model"]].append(r["metrics"].get("len", len(r["response"])))
        reason[r["model"]].append(int(bool(r.get("had_reasoning"))))

    out = {
        "n_runs": len(runs),
        "models": sorted({r["model"] for r in runs}),
        "realization_by_model": realization,
        "realization_by_model_type": type_summary,
        "decide_stance_by_model": decide_agreement,
        "synthesize_novelty_by_model": novelty_by_model,
        "mean_output_len_by_model": {m: round(sum(v) / len(v)) for m, v in verb.items()},
        "reasoning_fraction_by_model": {m: round(sum(v) / len(v), 2) for m, v in reason.items()},
    }
    OUT_PATH.write_text(json.dumps(out, indent=2, ensure_ascii=False))

    print(f"=== MVP analysis ({out['n_runs']} runs) ===\n")
    print("Realization rate (marker present) by model type:")
    for mt, d in type_summary.items():
        print(f"  {mt:>16}: " + "  ".join(f"{k}={v}" for k, v in d.items()))
    print("\nDecide stance by model (form still governing the verdict across models?):")
    for cid, d in decide_agreement.items():
        print(f"  [{cid}]")
        for m, c in d.items():
            print(f"    {m:>22}: {c}")
    print("\nSynthesize novelty (new-proposition rate) by model:")
    for m, v in novelty_by_model.items():
        print(f"  {m:>22}: {v}")
    print("\nMean output length / reasoning fraction by model:")
    for m in out["models"]:
        print(f"  {m:>22}: len={out['mean_output_len_by_model'].get(m)}  reasoning={out['reasoning_fraction_by_model'].get(m)}")
    print(f"\nWrote {OUT_PATH}")


if __name__ == "__main__":
    main()