"""pruner-dialectic — the realized control panel (v0.3.0).

Automated core: (purpose, content) -> form binding -> model routing -> run -> proxies.
Two human gates, exposed ONLY when their trigger fires:
  intent : purpose==decide AND contestedness r >= theta_r  -> bias-direction switch
  alpha  : synthesis S3 in borderline zone (nu>=nu_thr AND kop<=kop_thr) -> G/C/B verdict

Most runs expose 0 gates. The user does nothing unless a gate fires.

Usage:
    python -m runner.pruner_dialectic --purpose synthesize --content minimum_wage
    python -m runner.pruner_dialectic --purpose decide     --content pluto_planet
    python -m runner.pruner_dialectic --purpose decide     --content minimum_wage   # intent fires
    python -m runner.pruner_dialectic --purpose synthesize --content freshwater_alloc
    --auto        : auto-answer gates (intent=neutral, alpha=G) for non-interactive runs
    --no-run      : dry run (show routing + triggers, do not call the model)
"""
import argparse
import json
import sys
from pathlib import Path

from .forms import load_forms
from .llm import chat_meta

ROOT = Path(__file__).resolve().parent.parent
CFG_PATH = Path(__file__).resolve().parent / "dialectic_config.json"
DATASET = ROOT / "content" / "dataset.json"
EXP3_ITEMS = ROOT / "content" / "exp3_items.json"

# reuse alpha observables + the preserved-raw pool for nu
sys.path.insert(0, str(ROOT))
from analyze.analyze_alpha import (extract_synthesis, has_marker, refuses_binary,
                                    k_op, shingle, load_pool)

PURPOSE_TO_FORM = {
    "decide": "red_blue_debate",
    "synthesize": "dialectical_triad",
    "surface_assumptions": "socratic_dialogue",
}


def load_cfg():
    return json.loads(CFG_PATH.read_text())


def load_content(cid):
    items = {c["id"]: c for c in json.loads(DATASET.read_text())}
    items.update({c["id"]: c for c in json.loads(EXP3_ITEMS.read_text())})
    return items[cid]


def contestedness(cid, cfg):
    """r = Exp1 verdict divergence (1 - max label share) for the item, if known; else 0."""
    src = ROOT / cfg["contestedness_source"]
    if not src.exists():
        return 0.0
    d = json.loads(src.read_text())
    va = d.get("verdict_analysis", {})
    return float(va.get(cid, {}).get("divergence_score", 0.0))


def endpoint_for(cfg, which):
    return cfg["local_endpoint"] if which == "local" else cfg["cloud_endpoint"]


def run_model(cfg, model, which, prompt, seed):
    base = {
        "endpoint": endpoint_for(cfg, which),
        "api_key_env": cfg["api_key_env"],
        "model": model,
        "temperature": cfg["temperature"],
        "max_tokens": cfg["max_tokens"],
    }
    metas = chat_meta(prompt, base, seed=seed, n=1)
    return metas[0]["content"], metas[0]


def nu_against_pool(synthesis, content_id):
    """cross-model novelty vs preserved triad syntheses of the same item."""
    pool = [r for r in load_pool() if r["content_id"] == content_id]
    sh = shingle(synthesis)
    others = set()
    for r in pool:
        s = extract_synthesis(r["response"]) or r["response"][:300]
        others |= shingle(s)
    if not (sh | others):
        return 0.0
    return round(1 - len(sh & others) / len(sh | others), 3)


def gate_intent(cfg, content_id, r, auto):
    """Control #1: bias-direction switch. Returns one of scrutinize/include/neutral."""
    print("\n" + "=" * 64)
    print(f"[CONTROL #1 — intent]  contested item '{content_id}' (r={r:.3f} >= theta_r={cfg['theta_r']})")
    print("This is a contested decision: the model's verdict is model-dependent.")
    print("Which way do you want the decision pulled? (a value judgment — no correct answer)")
    print("  1) scrutinize   (conservative scrutiny, lean 'no')")
    print("  2) include       (incremental inclusion, lean 'yes')")
    print("  3) neutral       (let the reasoning model decide neutrally)")
    if auto:
        choice = "neutral"
        print(f"[auto] -> {choice}")
    else:
        c = input("choice [1/2/3, default 3]: ").strip() or "3"
        choice = {"1": "scrutinize", "2": "include", "3": "neutral"}.get(c, "neutral")
    return choice


def gate_alpha(cfg, synthesis, nu, kop, content_id, auto):
    """Control #2: authenticity gate. Returns G/C/B."""
    print("\n" + "=" * 64)
    print(f"[CONTROL #2 — alpha]  low-operational-concreteness synthesis (kop={kop} <= {cfg['alpha_kop_threshold']})")
    print("Automated proxies CANNOT decide genuineness (Stage B: nu is noise, kop is a weak proxy). You must judge.")
    print("\nSYNTHESIS:")
    print("  " + synthesis.replace("\n", "\n  "))
    print(f"\nobservables: nu={nu}  kop={kop}  (low kop = suspected cheap reframe)")
    print("  G = genuine third sublation   C = novelty-cheat (rhetoric, no mechanism)   B = borderline")
    if auto:
        v = "G"
        print(f"[auto] -> {v}")
    else:
        v = input("label [G/C/B, default G]: ").strip().upper() or "G"
        if v not in ("G", "C", "B"):
            v = "G"
    return v


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--purpose", required=True, choices=list(PURPOSE_TO_FORM))
    ap.add_argument("--content", required=True, help="content item id")
    ap.add_argument("--auto", action="store_true", help="auto-answer gates")
    ap.add_argument("--no-run", action="store_true", help="dry run, no model call")
    args = ap.parse_args()

    cfg = load_cfg()
    content = load_content(args.content)
    form_name = PURPOSE_TO_FORM[args.purpose]
    form_template = load_forms()[form_name]
    prompt = form_template.format(
        facts="\n".join(f"- {f}" for f in content["neutral_facts"]),
        question=content["contested_question"],
    )

    r = contestedness(args.content, cfg)
    intent_fires = (args.purpose == "decide" and r >= cfg["theta_r"])

    # --- routing (intent gate first, since it controls the model for decide-contested) ---
    intent_choice = None
    if intent_fires:
        intent_choice = gate_intent(cfg, args.content, r, args.auto)
        route_key = f"decide_contested_{intent_choice}"
    else:
        route_key = "decide_clear" if args.purpose == "decide" else args.purpose
    route = cfg["routing"][route_key]

    trace = {
        "purpose": args.purpose, "content": args.content, "form": form_name,
        "contestedness_r": round(r, 3), "intent_fires": intent_fires,
        "intent_choice": intent_choice, "route_key": route_key,
        "model": route["model"], "endpoint": route["endpoint"],
        "alpha_fires": None, "alpha_label": None, "rerouted": False,
    }

    print("\n=== pruner-dialectic ===")
    print(f"purpose={args.purpose}  content={args.content}  form={form_name}")
    print(f"contestedness r={r:.3f}  theta_r={cfg['theta_r']}  -> intent fires: {intent_fires}")
    print(f"routing: {route_key} -> {route['model']} ({route['endpoint']})")

    if args.no_run:
        print("\n[dry run] would call model then evaluate alpha trigger.")
        print(json.dumps(trace, indent=2))
        return

    # --- automated core: run ---
    print(f"\n[automated core] running {route['model']} ...")
    synthesis_full, meta = run_model(cfg, route["model"], route["endpoint"], prompt, cfg["seed"])
    synthesis = extract_synthesis(synthesis_full) or synthesis_full[:300]
    m = int(has_marker(synthesis_full))
    rho = int(refuses_binary(synthesis))
    kop = round(k_op(synthesis), 2)
    nu = nu_against_pool(synthesis, args.content)

    alpha_fires = (args.purpose == "synthesize" and kop <= cfg["alpha_kop_threshold"])
    trace.update({"m": m, "rho": rho, "nu": nu, "kop": kop, "alpha_fires": alpha_fires})
    print(f"proxies: m={m} rho={rho} nu={nu} kop={kop}  -> alpha fires: {alpha_fires}  (alpha scoped to synthesize; trigger kop<={cfg['alpha_kop_threshold']}; nu non-discriminating per Stage B)")

    # --- alpha gate ---
    if alpha_fires:
        label = gate_alpha(cfg, synthesis, nu, kop, args.content, args.auto)
        trace["alpha_label"] = label
        if label == "C":
            rr = cfg["routing"]["alpha_cheat_reroute"]
            print(f"\n[alpha=C] re-routing to stronger model: {rr['model']} ({rr['endpoint']})")
            synthesis_full, meta = run_model(cfg, rr["model"], rr["endpoint"], prompt, cfg["seed"])
            synthesis = extract_synthesis(synthesis_full) or synthesis_full[:300]
            trace["rerouted"] = True
            trace["reroute_model"] = rr["model"]
        elif label == "B":
            print("\n[alpha=B] you decide: accept (a) or re-run on stronger model (r)?")
            if auto_or_input(args.auto, "a", "r") == "r":
                rr = cfg["routing"]["alpha_cheat_reroute"]
                synthesis_full, _ = run_model(cfg, rr["model"], rr["endpoint"], prompt, cfg["seed"])
                synthesis = extract_synthesis(synthesis_full) or synthesis_full[:300]
                trace["rerouted"] = True
            else:
                print("[accept]")
        else:
            print("[alpha=G] accepted.")

    print("\n" + "=" * 64)
    print("FINAL SYNTHESIS:")
    print("  " + synthesis.replace("\n", "\n  "))
    print("\nTRACE:")
    print(json.dumps(trace, indent=2, ensure_ascii=False))


def auto_or_input(auto, *opts):
    if auto:
        return opts[0]
    return input(f"choice [{'/'.join(opts)}, default {opts[0]}]: ").strip() or opts[0]


if __name__ == "__main__":
    main()