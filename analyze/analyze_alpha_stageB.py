"""Alpha dissolution test — Stage B (human labels -> residual measurement).

Uses the 24 human-labeled candidates (G/B/C) to test whether alpha (authenticity)
dissolves into the observables (m, rho, nu, k_op):
  - authenticity score: G=2, B=1, C=0
  - does any observable (or a combination) separate G from C without residual?
  - if G and C are observationally indistinguishable on (m,rho,nu,k_op), alpha RESISTS
    -> alpha is a REAL control (keep); I_0 (full automation) confirmed phantom.
  - if observables perfectly separate G/C -> alpha DISSOLVES -> phantom (delete).

The key proof of residual: find G and C candidates with near-identical observables
(observational indistinguishability) -> no function of observables can separate them.
"""
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

from analyze.analyze_alpha import (load_pool, extract_synthesis, has_marker,
                                    refuses_binary, shingle, k_op, size_class)

DATA = Path(__file__).resolve().parent.parent / "data"
OUT = DATA / "alpha_dissolution_stageB.json"

# human labels (from the labeling session): index (1-based, sorted by kop asc, -nu desc) -> label
LABELS = {
    1: "G", 2: "G", 3: "B", 4: "C", 5: "C", 6: "C", 7: "B", 8: "C",
    9: "B", 10: "C", 11: "C", 12: "B", 13: "B", 14: "G", 15: "B", 16: "G",
    17: "B", 18: "C", 19: "G", 20: "C", 21: "C", 22: "C", 23: "G", 24: "B",
}
SCORE = {"G": 2, "B": 1, "C": 0}


def candidates():
    pool = load_pool()
    for r in pool:
        r["synthesis"] = extract_synthesis(r["response"]) or r["response"][:300]
        r["m"] = int(has_marker(r["response"]))
        r["rho"] = int(refuses_binary(r["synthesis"]))
        r["kop"] = round(k_op(r["synthesis"]), 2)
    by_item = defaultdict(list)
    for r in pool:
        by_item[r["content_id"]].append(r)
    for r in pool:
        sh = shingle(r["synthesis"])
        others = set()
        for q in by_item[r["content_id"]]:
            if q is not r:
                others |= shingle(q["synthesis"])
        r["nu"] = round(1 - (len(sh & others) / len(sh | others)) if (sh | others) else 0.0, 3)
    nus = sorted([r["nu"] for r in pool])
    kops = sorted([r["kop"] for r in pool])
    nu_hi = nus[2 * len(nus) // 3]
    kop_lo = kops[len(kops) // 3]
    cands = [r for r in pool if r["nu"] >= nu_hi and r["kop"] <= kop_lo]
    cands.sort(key=lambda r: (r["kop"], -r["nu"]))
    for i, r in enumerate(cands, 1):
        r["idx"] = i
        r["label"] = LABELS[i]
        r["score"] = SCORE[LABELS[i]]
    return cands


def main():
    cs = candidates()
    # per-label means
    by_lab = defaultdict(list)
    for r in cs:
        by_lab[r["label"]].append(r)
    means = {}
    for lab in ("G", "B", "C"):
        rs = by_lab[lab]
        means[lab] = {
            "n": len(rs),
            "m": round(float(np.mean([r["m"] for r in rs])), 3),
            "rho": round(float(np.mean([r["rho"] for r in rs])), 3),
            "nu": round(float(np.mean([r["nu"] for r in rs])), 4),
            "kop": round(float(np.mean([r["kop"] for r in rs])), 3),
        }

    # correlation of authenticity score with each observable
    scores = np.array([r["score"] for r in cs], dtype=float)
    def corr(obs):
        return round(float(np.corrcoef(scores, np.array([r[obs] for r in cs], dtype=float))[0, 1]), 3)
    corrmap = {o: corr(o) for o in ("m", "rho", "nu", "kop")}

    # best single-threshold separation G vs C (drop B): maximize accuracy
    gcs = [r for r in cs if r["label"] in ("G", "C")]
    best = {"obs": None, "thr": None, "acc": -1, "mis": []}
    for obs in ("m", "rho", "nu", "kop"):
        vals = sorted({r[obs] for r in gcs})
        for thr in vals:
            # predict G if obs >= thr (try both directions)
            for direction in (">=", "<="):
                correct = 0
                mis = []
                for r in gcs:
                    pred = "G" if (r[obs] >= thr if direction == ">=" else r[obs] <= thr) else "C"
                    if pred == r["label"]:
                        correct += 1
                    else:
                        mis.append(r["idx"])
                acc = correct / len(gcs)
                if acc > best["acc"]:
                    best = {"obs": obs, "thr": thr, "dir": direction, "acc": round(acc, 3),
                            "mis": mis, "n": len(gcs)}

    # observational indistinguishability: G and C with identical (m,rho) and |nu|<0.002 and |kop|<0.5
    indist = []
    for g in [r for r in cs if r["label"] == "G"]:
        for c in [r for r in cs if r["label"] == "C"]:
            if g["m"] == c["m"] and g["rho"] == c["rho"] \
               and abs(g["nu"] - c["nu"]) < 0.002 and abs(g["kop"] - c["kop"]) < 0.5:
                indist.append({"G": g["idx"], "C": c["idx"],
                               "obs": f"m={g['m']},rho={g['rho']},nu~{g['nu']},kop~{g['kop']}"})

    # logistic combination (G vs C) on all 4 observables
    try:
        from sklearn.linear_model import LogisticRegression
        X = np.array([[r["m"], r["rho"], r["nu"], r["kop"]] for r in gcs], dtype=float)
        y = np.array([1 if r["label"] == "G" else 0 for r in gcs])
        clf = LogisticRegression(max_iter=2000).fit(X, y)
        pred = clf.predict(X)
        combo_acc = round(float((pred == y).mean()), 3)
        combo_mis = [gcs[i]["idx"] for i in range(len(gcs)) if pred[i] != y[i]]
    except Exception:
        combo_acc, combo_mis = None, []

    # G cases that a kop-only "cheat detector" (kop low -> C) would MISFLAG
    kop_cheat_misflag_G = [r["idx"] for r in cs if r["label"] == "G" and r["kop"] <= 1.0]

    out = {
        "n_labeled": len(cs),
        "label_counts": {lab: len(by_lab[lab]) for lab in ("G", "B", "C")},
        "per_label_means": means,
        "authenticity_score_correlation": corrmap,
        "best_single_threshold_GvsC": best,
        "logistic_combo_GvsC_accuracy": combo_acc,
        "logistic_combo_GvsC_misclassified": combo_mis,
        "observational_indistinguishable_GC_pairs": indist,
        "G_misflagged_by_low_kop": kop_cheat_misflag_G,
        "verdict": None,  # filled below
    }

    # verdict: residual if indistinguishable pairs exist OR combo can't reach 100%
    residual = bool(indist) or (combo_acc is not None and combo_acc < 1.0)
    out["verdict"] = "RESISTS (alpha is REAL -> keep control; I_0 full-automation = phantom)" if residual \
        else "DISSOLVES (alpha is PHANTOM -> delete control; I_0 full-automation recovers)"
    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False))

    print(f"=== Alpha dissolution Stage B ({len(cs)} labeled) ===\n")
    print("Label counts:", out["label_counts"])
    print("\nPer-label observable means:")
    print(f"{'label':>6} {'n':>3} {'m':>5} {'rho':>5} {'nu':>7} {'kop':>6}")
    for lab in ("G", "B", "C"):
        a = means[lab]
        print(f"{lab:>6} {a['n']:>3} {a['m']:>5} {a['rho']:>5} {a['nu']:>7} {a['kop']:>6}")
    print("\nAuthenticity-score correlation with observables:", corrmap)
    print(f"\nBest single-threshold G-vs-C: obs={best['obs']} thr={best['thr']} dir={best['dir']} acc={best['acc']} ({best['n']}) mis={best['mis']}")
    print(f"Logistic combo (m,rho,nu,kop) G-vs-C accuracy: {combo_acc}  misclassified: {combo_mis}")
    print(f"\nObservationally-indistinguishable G/C pairs: {len(indist)}")
    for p in indist[:8]:
        print(f"  G#{p['G']} <-> C#{p['C']}  ({p['obs']})")
    print(f"\nG cases misflagged as cheat by low-kop (kop<=1.0): {kop_cheat_misflag_G}")
    print(f"\nVERDICT: {out['verdict']}")
    print(f"\nWrote {OUT}")


if __name__ == "__main__":
    main()