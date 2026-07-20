"""pruner-dialectic — the realized control panel (v0.3.0), interactive.

Two modes:
  INTERACTIVE (default when no problem args): a conversational REPL.
    The user types in the problem (purpose, question, facts) from outside, the
    automated core runs, and the two human gates surface as conversational prompts
    only when their trigger fires. Loops for multiple problems.
  ARG mode: --purpose/--content (preset) or --question/--fact (ad-hoc from outside).

Automated core: (purpose, content) -> form binding -> model routing -> run -> proxies.
Two human gates, exposed ONLY when their trigger fires:
  intent : purpose==decide AND contestedness r >= theta_r        -> bias-direction switch
  alpha  : purpose==synthesize AND kop <= alpha_kop_threshold     -> G/C/B verdict
Most runs expose 0 gates.

Usage:
    python -m runner.pruner_dialectic                       # interactive REPL
    python -m runner.pruner_dialectic --purpose synthesize --content minimum_wage
    python -m runner.pruner_dialectic --purpose decide --question "..." --fact "..." --fact "..."
    --auto   : auto-answer gates (non-interactive)
    --no-run : dry run (routing + triggers only, no model call)
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

sys.path.insert(0, str(ROOT))
from analyze.analyze_alpha import (extract_synthesis, has_marker, refuses_binary,
                                    k_op, shingle, load_pool)

PURPOSE_TO_FORM = {
    "decide": "red_blue_debate",
    "synthesize": "dialectical_triad",
    "surface_assumptions": "socratic_dialogue",
}
PURPOSE_LABELS = {"1": "decide", "2": "synthesize", "3": "surface_assumptions"}


# ---------- config / content ----------

def load_cfg():
    return json.loads(CFG_PATH.read_text())


def load_preset_content(cid):
    items = {c["id"]: c for c in json.loads(DATASET.read_text())}
    items.update({c["id"]: c for c in json.loads(EXP3_ITEMS.read_text())})
    if cid not in items:
        raise SystemExit(f"unknown content id: {cid}")
    return items[cid]


def contestedness(cid, cfg, r_override=None):
    if r_override is not None:
        return float(r_override)
    src = ROOT / cfg["contestedness_source"]
    if not src.exists():
        return 0.0
    d = json.loads(src.read_text())
    return float(d.get("verdict_analysis", {}).get(cid, {}).get("divergence_score", 0.0))


def endpoint_for(cfg, which):
    return cfg["local_endpoint"] if which == "local" else cfg["cloud_endpoint"]


def run_model(cfg, model, which, prompt, seed):
    base = {"endpoint": endpoint_for(cfg, which), "api_key_env": cfg["api_key_env"],
            "model": model, "temperature": cfg["temperature"], "max_tokens": cfg["max_tokens"]}
    metas = chat_meta(prompt, base, seed=seed, n=1)
    return metas[0]["content"]


def nu_against_pool(synthesis, content_id):
    pool = [r for r in load_pool() if r["content_id"] == content_id]
    sh = shingle(synthesis)
    others = set()
    for r in pool:
        others |= shingle(extract_synthesis(r["response"]) or r["response"][:300])
    return round(1 - len(sh & others) / len(sh | others), 3) if (sh | others) else 0.0


# ---------- gates (conversational) ----------

def gate_intent(cfg, content_id, r, auto):
    print("\n" + "=" * 64)
    print(f"[CONTROL #1 — intent]  contested decision '{content_id}' (r={r:.3f} >= theta_r={cfg['theta_r']})")
    print("이 결정은 모델 의존적(정답이 열려있음). 어느 쪽으로 당기시겠습니까?")
    print("  1) scrutinize   (보수 검증, lean 'no')")
    print("  2) include      (점진 포용, lean 'yes')")
    print("  3) neutral      (중립)")
    if auto:
        c = "neutral"; print(f"[auto] -> {c}"); return c
    c = input("choice [1/2/3, default 3]: ").strip() or "3"
    return {"1": "scrutinize", "2": "include", "3": "neutral"}.get(c, "neutral")


def gate_alpha(cfg, synthesis, nu, kop, auto):
    print("\n" + "=" * 64)
    print(f"[CONTROL #2 — alpha]  저-작동구조 종합 (kop={kop} <= {cfg['alpha_kop_threshold']})")
    print("자동 프록시는 진정성을 판정 못 함(Stage B: nu는 노이즈, kop는 약한 프록시). 사람이 판정.")
    print("\n종합:")
    print("  " + synthesis.replace("\n", "\n  "))
    print(f"\n관측량: nu={nu}  kop={kop}  (kop 낮을수록 값싼 재구성 의심)")
    print("  G=진짜 제3 지양  C=novelty-cheat(수사, 메커니즘 없음)  B=경계")
    if auto:
        v = "G"; print(f"[auto] -> {v}"); return v
    v = (input("label [G/C/B, default G]: ").strip().upper() or "G")
    return v if v in ("G", "C", "B") else "G"


def ask(prompt, default=None):
    s = input(prompt).strip()
    return s if s else default


# ---------- one full run ----------

def run_one(cfg, purpose, content, r_override, auto, no_run):
    cid = content["id"]
    form_name = PURPOSE_TO_FORM[purpose]
    form_template = load_forms()[form_name]
    prompt = form_template.format(
        facts="\n".join(f"- {f}" for f in content["neutral_facts"]),
        question=content["contested_question"],
    )
    r = contestedness(cid, cfg, r_override)
    intent_fires = (purpose == "decide" and r >= cfg["theta_r"])

    intent_choice = None
    if intent_fires:
        intent_choice = gate_intent(cfg, cid, r, auto)
        route_key = f"decide_contested_{intent_choice}"
    else:
        route_key = "decide_clear" if purpose == "decide" else purpose
    route = cfg["routing"][route_key]

    trace = {"purpose": purpose, "content": cid, "form": form_name,
             "contestedness_r": round(r, 3), "intent_fires": intent_fires,
             "intent_choice": intent_choice, "route_key": route_key,
             "model": route["model"], "endpoint": route["endpoint"],
             "alpha_fires": None, "alpha_label": None, "rerouted": False}

    print("\n=== pruner-dialectic ===")
    print(f"purpose={purpose}  content={cid}  form={form_name}")
    print(f"contestedness r={r:.3f}  theta_r={cfg['theta_r']}  -> intent fires: {intent_fires}")
    print(f"routing: {route_key} -> {route['model']} ({route['endpoint']})")

    if no_run:
        print("\n[dry run] 모델 호출 생략.")
        print(json.dumps(trace, indent=2, ensure_ascii=False))
        return

    print(f"\n[automated core] running {route['model']} ...")
    full = run_model(cfg, route["model"], route["endpoint"], prompt, cfg["seed"])
    synthesis = extract_synthesis(full) or full[:300]
    m = int(has_marker(full)); rho = int(refuses_binary(synthesis))
    kop = round(k_op(synthesis), 2); nu = nu_against_pool(synthesis, cid)
    alpha_fires = (purpose == "synthesize" and kop <= cfg["alpha_kop_threshold"])
    trace.update({"m": m, "rho": rho, "nu": nu, "kop": kop, "alpha_fires": alpha_fires})
    print(f"proxies: m={m} rho={rho} nu={nu} kop={kop}  -> alpha fires: {alpha_fires}")

    if alpha_fires:
        label = gate_alpha(cfg, synthesis, nu, kop, auto)
        trace["alpha_label"] = label
        if label == "C":
            rr = cfg["routing"]["alpha_cheat_reroute"]
            print(f"\n[alpha=C] 강한 모델로 재라우팅: {rr['model']} ({rr['endpoint']})")
            full = run_model(cfg, rr["model"], rr["endpoint"], prompt, cfg["seed"])
            synthesis = extract_synthesis(full) or full[:300]
            trace["rerouted"] = True; trace["reroute_model"] = rr["model"]
        elif label == "B":
            print("\n[alpha=B] 결정: a=수용, r=강한 모델로 재실행")
            if (ask("choice [a/r, default a]: ", "a") if not auto else "a") == "r":
                rr = cfg["routing"]["alpha_cheat_reroute"]
                full = run_model(cfg, rr["model"], rr["endpoint"], prompt, cfg["seed"])
                synthesis = extract_synthesis(full) or full[:300]
                trace["rerouted"] = True
            else:
                print("[수용]")
        else:
            print("[alpha=G] 수용.")

    print("\n" + "=" * 64)
    print("최종 종합/결과:")
    print("  " + synthesis.replace("\n", "\n  "))
    print("\nTRACE:")
    print(json.dumps(trace, indent=2, ensure_ascii=False))


# ---------- interactive REPL ----------

def interactive(cfg, auto, no_run):
    print("=" * 64)
    print("pruner-dialectic — 대화형 제어판 (v0.3.0)")
    print("문제를 직접 입력하세요. 게이트는 트리거될 때만 물어봅니다.")
    print("=" * 64)
    while True:
        try:
            print("\n--- 새 문제 ---")
            pc = ask("목적? 1) decide  2) synthesize  3) surface_assumptions  [1/2/3]: ", "2")
            purpose = PURPOSE_LABELS.get(pc, "synthesize")
            question = ask("질문(한 줄): ")
            if not question:
                print("질문이 필요합니다."); continue
            print("사실을 한 줄씩 입력 (빈 줄로 종료):")
            facts = []
            while True:
                f = input("  - ").strip()
                if not f:
                    break
                facts.append(f)
            if not facts:
                print("사실이 최소 1개 필요합니다."); continue
            r_override = None
            if purpose == "decide":
                contested = ask("이 결정은 쟁점인가요(어느 쪽이 정답인지 열려있는)? [y/n, default y]: ", "y")
                r_override = 0.5 if contested.lower().startswith("y") else 0.0
            content = {"id": "adhoc", "domain": "user", "neutral_facts": facts,
                       "contested_question": question}
            run_one(cfg, purpose, content, r_override, auto, no_run)
            again = ask("\n다른 문제? [y/n, default n]: ", "n")
            if not again.lower().startswith("y"):
                print("종료."); break
        except (KeyboardInterrupt, EOFError):
            print("\n종료."); break


# ---------- arg mode / dispatch ----------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--purpose", choices=list(PURPOSE_TO_FORM))
    ap.add_argument("--content", help="preset content item id")
    ap.add_argument("--question", help="ad-hoc question (external problem)")
    ap.add_argument("--fact", action="append", default=[], help="ad-hoc fact (repeatable)")
    ap.add_argument("--r", type=float, help="override contestedness 0..1")
    ap.add_argument("--auto", action="store_true", help="auto-answer gates")
    ap.add_argument("--no-run", action="store_true", help="dry run, no model call")
    args = ap.parse_args()

    cfg = load_cfg()
    if not args.purpose and not args.content and not args.question:
        interactive(cfg, args.auto, args.no_run)
        return

    if not args.purpose:
        ap.error("--purpose required in arg mode")
    if args.question:
        content = {"id": "adhoc", "domain": "user",
                   "neutral_facts": args.fact or ["(no facts provided)"],
                   "contested_question": args.question}
    elif args.content:
        content = load_preset_content(args.content)
    else:
        ap.error("provide --content (preset) or --question (ad-hoc)")
    run_one(cfg, args.purpose, content, args.r, args.auto, args.no_run)


if __name__ == "__main__":
    main()