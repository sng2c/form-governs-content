"""Alpha dissolution test — Stage A (no labels; observables only).

Pools every dialectical-triad synthesis from the preserved raw runs:
  - raw_runs.jsonl  (Exp1: form==dialectical_triad, gpt-oss:120b)
  - mvp_runs.jsonl  (Exp2: purpose==synthesize -> dialectical_triad, 8 models)
  - exp3_runs.jsonl (Exp3: form==dialectical_triad, 5 local models 1B-12B)

Computes observables per synthesis:
  m   = SYNTHESIS CONCLUSION marker present
  rho = refuses the binary (not a bare yes/no)
  nu  = novelty = 1 - shingle-Jaccard vs the union of OTHER syntheses of the same item
        (how idiosyncratic this synthesis is vs the cross-model consensus on the item)
  k_op = operational concreteness = density of mechanism/working-structure terms
        (the PRUNER_LOG-L3 refinement: NOT proper nouns, but operational verbs/structure).

Tests:
  1. Do observables vary by model size? Does k_op separate 1B (suspected cheap novelty)?
  2. PRUNER_LOG claim: nu <-> k_op inverse correlation?
  3. Surface high-nu + low-k_op candidates (suspected novelty-cheats) for the human gate.

This is the v0.3.0 descent on the alpha candidate control: does alpha dissolve into
observables, or is there a residual? Stage A only asks whether the observables CARRY the
authenticity signal; Stage B (human labels) will measure the residual.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

import numpy as np

DATA = Path(__file__).resolve().parent.parent / "data"
OUT = DATA / "alpha_dissolution_stageA.json"

# operational / working-structure terms (mechanism description, not rhetoric)
KOP = [
    # mechanism nouns
    "mechanism", "system", "framework", "process", "procedure", "schedule",
    "threshold", "quota", "tier", "phase", "index", "floor", "mandate", "gate",
    "allocation", "calibration", "pipeline", "registry", "subsidy", "credit",
    "tax", "bond", "standard", "criterion", "metric", "regulator", "governance",
    "oversight", "audit", "review", "pilot", "trial", "rollout", "incentive",
    "penalty", "instrument", "safeguard", "guardrail", "indicator", "dashboard",
    # operational verbs
    "allocate", "calibrate", "route", "phase", "tier", "mandate", "implement",
    "enforce", "monitor", "adjust", "scale", "distribute", "weight", "transition",
    "redesign", "reconfigure", "integrate", "orchestrate", "coordinate", "sequence",
    "stage", "peg", "cap", "grant", "revoke", "certify", "license", "index",
    # operational adjectives
    "dynamic", "adaptive", "weighted", "staged", "conditional", "real-time",
    "participatory", "indexed", "tiered", "phased", "modular", "recursive",
    "proportional", "graduated", "differentiated",
]


def extract_synthesis(text):
    m = re.search(r"SYNTHESIS CONCLUSION:\s*(.+)", text, re.I | re.S)
    return m.group(1).strip().strip('"').strip() if m else None


def has_marker(text):
    return bool(re.search(r"SYNTHESIS CONCLUSION:", text, re.I))


def refuses_binary(text):
    t = text.lower()
    bare_yes = bool(re.search(r"\byes\b", t)) and not re.search(r"\bno\b", t)
    bare_no = bool(re.search(r"\bno\b", t)) and not re.search(r"\byes\b", t)
    return not (bare_yes or bare_no)


def shingle(s, k=3):
    s = s.lower().split()
    return set(tuple(s[i:i + k]) for i in range(len(s) - k + 1)) if len(s) >= k else {tuple(s)}


def k_op(text):
    t = text.lower()
    words = len(t.split())
    if words == 0:
        return 0.0
    hits = sum(t.count(w) for w in KOP)
    return 100.0 * hits / words


def size_class(model):
    m = model.lower()
    if "1b" in m:
        return "1B"
    if "3b" in m:
        return "3B"
    if "4b" in m:
        return "4B"
    if "12b" in m:
        return "12B"
    if "20b" in m:
        return "20B"
    if "120b" in m:
        return "120B"
    if "397b" in m or "675b" in m or "671b" in m or "1t" in m:
        return "400B+"
    return "?"


def load_pool():
    pool = []
    # Exp1
    p = DATA / "raw_runs.jsonl"
    if p.exists():
        for r in (json.loads(l) for l in p.read_text().splitlines() if l.strip()):
            if r.get("form") == "dialectical_triad":
                pool.append({"source": "exp1", "model": "gpt-oss:120b",
                             "content_id": r["content_id"], "response": r["response"]})
    # Exp2
    p = DATA / "mvp_runs.jsonl"
    if p.exists():
        for r in (json.loads(l) for l in p.read_text().splitlines() if l.strip()):
            if r.get("purpose") == "synthesize":
                pool.append({"source": "exp2", "model": r["model"],
                             "content_id": r["content_id"], "response": r["response"]})
    # Exp3
    p = DATA / "exp3_runs.jsonl"
    if p.exists():
        for r in (json.loads(l) for l in p.read_text().splitlines() if l.strip()):
            if r.get("form") == "dialectical_triad":
                pool.append({"source": "exp3", "model": r["model"],
                             "content_id": r["content_id"], "response": r["response"]})
    return pool


def main():
    pool = load_pool()
    for r in pool:
        r["synthesis"] = extract_synthesis(r["response"]) or r["response"][:300]
        r["m"] = int(has_marker(r["response"]))
        r["rho"] = int(refuses_binary(r["synthesis"]))
        r["kop"] = round(k_op(r["synthesis"]), 2)

    # novelty vs other syntheses of the same content_id
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

    # per size-class aggregates
    by_size = defaultdict(list)
    for r in pool:
        by_size[size_class(r["model"])].append(r)
    size_agg = {}
    for sz, rs in by_size.items():
        size_agg[sz] = {
            "n": len(rs),
            "m": round(np.mean([r["m"] for r in rs]), 3),
            "rho": round(np.mean([r["rho"] for r in rs]), 3),
            "nu": round(np.mean([r["nu"] for r in rs]), 3),
            "kop": round(np.mean([r["kop"] for r in rs]), 3),
        }

    # nu <-> kop correlation (the PRUNER_LOG claim)
    nus = [r["nu"] for r in pool]
    kops = [r["kop"] for r in pool]
    corr = round(float(np.corrcoef(nus, kops)[0, 1]), 3) if len(pool) > 2 else 0.0

    # candidate cheats: high nu (top 1/3) AND low kop (bottom 1/3)
    nu_sorted = sorted(nus)
    kop_sorted = sorted(kops)
    nu_hi = nu_sorted[2 * len(nu_sorted) // 3]
    kop_lo = kop_sorted[len(kop_sorted) // 3]
    candidates = [r for r in pool if r["nu"] >= nu_hi and r["kop"] <= kop_lo]
    candidates.sort(key=lambda r: (r["kop"], -r["nu"]))

    out = {
        "n_syntheses": len(pool),
        "size_class_aggregates": size_agg,
        "nu_kop_correlation": corr,
        "nu_hi_threshold": nu_hi,
        "kop_lo_threshold": kop_lo,
        "candidate_cheats_n": len(candidates),
        "candidate_cheats": [
            {"model": r["model"], "size": size_class(r["model"]),
             "content_id": r["content_id"], "m": r["m"], "rho": r["rho"],
             "nu": r["nu"], "kop": r["kop"], "synthesis": r["synthesis"][:220]}
            for r in candidates
        ],
    }
    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False))

    print(f"=== Alpha dissolution Stage A ({len(pool)} triad syntheses) ===\n")
    print("Per size-class (m=marker, rho=refuse_binary, nu=novelty, kop=operational concreteness):")
    print(f"{'size':>6} {'n':>4} {'m':>5} {'rho':>5} {'nu':>6} {'kop':>6}")
    for sz, a in sorted(size_agg.items()):
        print(f"{sz:>6} {a['n']:>4} {a['m']:>5} {a['rho']:>5} {a['nu']:>6} {a['kop']:>6}")
    print(f"\nnu <-> kop correlation: {corr}  (PRUNER_LOG claim: inverse; negative supports it)")
    print(f"\nCandidate novelty-cheats (high nu >= {nu_hi} AND low kop <= {kop_lo}): {len(candidates)}")
    for r in candidates[:12]:
        print(f"  [{r['model']} ({size_class(r['model'])})] {r['content_id']}  nu={r['nu']} kop={r['kop']}  m={r['m']} rho={r['rho']}")
        print(f"     {r['synthesis']}")
    print(f"\nWrote {OUT}")


if __name__ == "__main__":
    main()