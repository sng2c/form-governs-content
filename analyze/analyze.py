"""Compute the core Hegel test: does form govern content?

For each content_item we have, for each form, n_repeats conclusion strings.
We embed conclusions and compute:

  - within_form_variance:   mean pairwise cosine distance among repeats of same form.
  - across_form_variance:   mean pairwise cosine distance between conclusions of
                             DIFFERENT forms (same content item).
  - ratio = across / within : if >> 1, form governs content (Hegel H1 holds).
                             if ~ 1, form is cosmetic (H0).

We also compute, per form family (rearrangement vs generative):
  - mean within-form variance
  - novelty rate: fraction of conclusions whose nearest non-own repeat is in a
    DIFFERENT content item (a loose proxy) — here we instead measure how often
    a conclusion contains a proposition not present in any other form's
    conclusion of the same item (set-difference on lowercased token shingles).
"""
import json
from itertools import combinations
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_distances

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
RAW_PATH = DATA_DIR / "raw_runs.jsonl"
OUT_PATH = DATA_DIR / "analysis.json"


def load_runs():
    return [json.loads(l) for l in RAW_PATH.read_text().splitlines() if l.strip()]


def embed(conclusions: list[str]) -> np.ndarray:
    # TF-IDF as a cheap, deterministic, style-agnostic-ish embedding.
    # (Swap for sentence-transformers later if available.)
    vec = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True, stop_words="english")
    X = vec.fit_transform(conclusions).toarray()
    # normalize
    norms = np.linalg.norm(X, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return X / norms


def embed_pair(conclusions_a: list[str], conclusions_b: list[str]):
    """Embed two groups with a SHARED vocabulary so the dimensions match
    (required by cosine_distances)."""
    vec = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True, stop_words="english")
    vec.fit(conclusions_a + conclusions_b)

    def to_mat(cs):
        X = vec.transform(cs).toarray()
        n = np.linalg.norm(X, axis=1, keepdims=True)
        n[n == 0] = 1.0
        return X / n

    return to_mat(conclusions_a), to_mat(conclusions_b)


def mean_pairwise_distance(rows):
    if len(rows) < 2:
        return 0.0
    X = embed([r["conclusion"] for r in rows])
    d = cosine_distances(X)
    n = len(rows)
    return float(d[np.triu_indices(n, k=1)].mean())


def shingle(s, k=3):
    s = s.lower().split()
    return set(tuple(s[i : i + k]) for i in range(len(s) - k + 1)) if len(s) >= k else {tuple(s)}


def novelty_rate(item_rows):
    # NB: see verdict-level novelty below; this shingle version is a coarse proxy.
    """For each form, fraction of its conclusions whose shingles are not a subset of
    the union of OTHER forms' conclusion shingles (proxy for a novel proposition).
    Returns {form: rate}.
    """
    by_form = {}
    for r in item_rows:
        by_form.setdefault(r["form"], []).append(r["conclusion"])
    out = {}
    for f, concl in by_form.items():
        others = set()
        for g, cs in by_form.items():
            if g == f:
                continue
            for c in cs:
                others |= shingle(c)
        cnt = 0
        for c in concl:
            sh = shingle(c)
            if sh and not sh.issubset(others):
                cnt += 1
        out[f] = cnt / max(1, len(concl))
    return out


# ---- Verdict-level (style-stripped) content analysis -------------------------
# The TF-IDF ratio is style-leaky for a reasoning model (surface words vary a lot
# even repeating the same form). The cleaner test: classify each conclusion into
# a normalized stance label per item, then see whether FORMS DISAGREE on the
# verdict for the same content. Verdict divergence = form governing *content*.

import re as _re


def classify_verdict(conclusion: str, content_id: str) -> str:
    """Item-specific stance classifier (pilot heuristic). Returns a short label."""
    t = conclusion.lower()
    neg = any(w in t for w in ["not contingent", "without waiting", "proceed without",
                              "not mandate", "should not", "does not", "do not support",
                              "no,", "oppose", "against", "keep dwarf", "stays a dwarf",
                              "remains a dwarf", "does not unequivocally"])
    pos = any(w in t for w in ["supports raising", "support raising", "supports a",
                              "favor", "favors", "reclassify", "reclassified as a full",
                              "reinstated as a planet", "is a planet", "promote to planet",
                              "enforce a 2035", "enforce the 2035", "should raise"])
    qual = any(w in t for w in ["mixed", "qualified", "conditional", "only if",
                                "if revised", "pending", "calibrated", "gradual",
                                "with safeguards", "multi-criterion", "dual-criterion",
                                "refined"])
    if content_id == "pluto_planet":
        if any(w in t for w in ["keep dwarf", "stays a dwarf", "remains a dwarf",
                               "stays dwarf", "dwarf planet for now"]):
            return "keep_dwarf"
        if pos and not neg:
            return "reclassify"
        if qual:
            return "conditional"
        return "reclassify"
    if content_id == "minimum_wage":
        if neg and not pos:
            return "oppose"
        if pos and not neg:
            return "support"
        if qual:
            return "qualified"
        if pos:
            return "support"
        return "qualified"
    if content_id == "battery_limits":
        # question = should phase-out be CONTINGENT on aviation-grade density?
        if any(w in t for w in ["not contingent", "without waiting", "proceed without",
                               "proceed by 2035", "enforce a 2035", "enforce the 2035",
                               "not condition", "not mandate a phase-out on"]):
            return "no_contingency"
        if any(w in t for w in ["contingent", "first reach", "prerequisite", "wait for"]):
            return "pro_contingency"
        return "no_contingency"
    return "other"


def verdict_analysis(runs):
    """For each item, compute the verdict distribution across forms and a
    divergence score = 1 - max_label_share (0=all forms agree, near 1=split)."""
    by_item = {}
    for r in runs:
        by_item.setdefault(r["content_id"], []).append(r)
    out = {}
    all_div = []
    for item, rows in by_item.items():
        labels = [classify_verdict(r["conclusion"], item) for r in rows]
        # per form, the modal label and its share
        from collections import Counter, defaultdict
        per_form = {}
        form_labels = defaultdict(list)
        for r, lab in zip(rows, labels):
            form_labels[r["form"]].append(lab)
        for f, labs in form_labels.items():
            c = Counter(labs)
            modal, modal_n = c.most_common(1)[0]
            per_form[f] = {"modal_label": modal, "modal_share": modal_n / len(labs),
                          "labels": dict(c)}
        overall = Counter(labels)
        total = len(labels)
        max_share = max(overall.values()) / total
        divergence = 1 - max_share
        all_div.append(divergence)
        out[item] = {
            "verdict_distribution": dict(overall),
            "divergence_score": round(divergence, 3),
            "per_form": per_form,
        }
    out["_overall_divergence"] = round(float(np.mean(all_div)), 3) if all_div else 0.0
    return out


def main():
    from analyze.extract import extract_all
    from runner.forms import family

    runs = load_runs()
    runs = extract_all(runs)

    items = sorted({r["content_id"] for r in runs})

    results = {"by_item": {}, "overall": {}}

    all_within = []
    all_across = []
    family_within = {"rearrangement": [], "generative": []}
    family_novel = {"rearrangement": [], "generative": []}

    for item in items:
        rows = [r for r in runs if r["content_id"] == item]
        forms = sorted({r["form"] for r in rows})

        within = {}
        for f in forms:
            w = mean_pairwise_distance([r for r in rows if r["form"] == f])
            within[f] = w
            all_within.append(w)
            family_within[family(f)].append(w)

        # across-form: for each pair of forms, mean distance between their conclusions
        across_pairs = []
        for a, b in combinations(forms, 2):
            ra = [r for r in rows if r["form"] == a]
            rb = [r for r in rows if r["form"] == b]
            Xa, Xb = embed_pair([x["conclusion"] for x in ra], [x["conclusion"] for x in rb])
            d = cosine_distances(Xa, Xb)
            across_pairs.append(float(d.mean()))
            all_across.append(d.mean())

        within_mean = float(np.mean(list(within.values()))) if within else 0.0
        across_mean = float(np.mean(across_pairs)) if across_pairs else 0.0
        ratio = across_mean / within_mean if within_mean > 1e-9 else float("inf")

        nov = novelty_rate(rows)  # {form: rate}
        for f, rate in nov.items():
            family_novel[family(f)].append(rate)

        results["by_item"][item] = {
            "within_form_variance": within,
            "across_form_variance": across_mean,
            "ratio_across_over_within": ratio,
            "novelty_by_form": nov,
        }

    overall_within = float(np.mean(all_within)) if all_within else 0.0
    overall_across = float(np.mean(all_across)) if all_across else 0.0
    results["overall"] = {
        "within_form_variance": overall_within,
        "across_form_variance": overall_across,
        "ratio_across_over_within": overall_across / overall_within if overall_within > 1e-9 else float("inf"),
        "hegel_h1_holds": overall_across / overall_within > 1.5 if overall_within > 1e-9 else True,
        "family_within_variance": {
            fam: float(np.mean(v)) if v else 0.0 for fam, v in family_within.items()
        },
        "family_novelty_rate": {
            fam: float(np.mean(v)) if v else 0.0 for fam, v in family_novel.items()
        },
    }

    # Style-stripped verdict analysis (the cleaner Hegel test for noisy text).
    results["verdict_analysis"] = verdict_analysis(runs)
    va = results["verdict_analysis"]["_overall_divergence"]
    results["overall"]["verdict_divergence"] = va
    results["overall"]["hegel_h1_verdict"] = va > 0.15

    OUT_PATH.write_text(json.dumps(results, indent=2))
    print(json.dumps(results["overall"], indent=2))
    print("\nVerdict analysis (per item):")
    for item, v in results["verdict_analysis"].items():
        if item.startswith("_"):
            continue
        print(f"  {item}: divergence={v['divergence_score']} dist={v['verdict_distribution']}")
    print(f"\nWrote {OUT_PATH}")


if __name__ == "__main__":
    main()