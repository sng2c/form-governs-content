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
KOREAN_PURPOSE = {"decide": "결정", "synthesize": "종합", "surface_assumptions": "전제 드러내기"}
KOREAN_FORM = {"red_blue_debate": "찬반토론", "dialectical_triad": "변증법 삼단", "socratic_dialogue": "소크라테스 대화"}


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
    print(f"[사람 개입 1 — 결정 방향]  의견이 갈리는 결정 '{content_id}' (의견 갈림 정도 r={r:.3f} ≥ 기준 {cfg['theta_r']})")
    print("이 결정은 정답이 열려 있어 모델이 어느 쪽으로든 갈 수 있습니다. 어느 쪽으로 당기시겠습니까?")
    print("  1) 보수 검증  (아니오 쪽으로 신중하게 따짐)")
    print("  2) 점진 포용  (예 쪽으로 조심스럽게 받아들임)")
    print("  3) 중립      (모델이 스스로 판단)")
    if auto:
        c = "neutral"; print(f"[자동] -> 3) 중립"); return c
    c = input("선택 [1/2/3, 기본 3]: ").strip() or "3"
    return {"1": "scrutinize", "2": "include", "3": "neutral"}.get(c, "neutral")


def gate_alpha(cfg, synthesis, nu, kop, auto):
    print("\n" + "=" * 64)
    print(f"[사람 개입 2 — 진정성 판정]  작동 구조가 부실한 종합 (kop={kop} ≤ 기준 {cfg['alpha_kop_threshold']})")
    print("자동 지표로는 진짜/가짜를 가릴 수 없습니다(Stage B 검증). 사람이 판정해 주세요.")
    print("\n종합 내용:")
    print("  " + synthesis.replace("\n", "\n  "))
    print(f"\n지표: nu(새로움)={nu}  kop(작동구조 밀도)={kop}  — kop가 낮을수록 겉치레 수사 의심)")
    print("  1) 진짜   (양극을 넘어선 제3의 종합/지양)")
    print("  2) 겉치레 (수사적 재구성, 작동 메커니즘 없음)")
    print("  3) 애매함")
    if auto:
        v = "G"; print(f"[자동] -> 1) 진짜"); return v
    c = input("판정 [1/2/3, 기본 1]: ").strip() or "1"
    return {"1": "G", "2": "C", "3": "B"}.get(c, "G")


def ask(prompt, default=None):
    s = input(prompt).strip()
    return s if s else default


def paste_until_dot(prompt):
    """Read pasted lines until a line that is just '.' (the terminator).
    Lets the user paste a multi-line block (question or facts) and end with a lone '.' line."""
    print(prompt)
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip() == ".":
            break
        lines.append(line)
    return lines


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
    print(f"목적={KOREAN_PURPOSE[purpose]}({purpose})  문제={cid}  형식={KOREAN_FORM[form_name]}")
    print(f"의견 갈림 정도 r={r:.3f}  기준={cfg['theta_r']}  -> 방향 게이트 발동: {intent_fires}")
    print(f"라우팅: {route_key} -> {route['model']} ({'로컬' if route['endpoint']=='local' else '클라우드'})")

    if no_run:
        print("\n[미리보기] 모델 호출 생략.")
        print(json.dumps(trace, indent=2, ensure_ascii=False))
        return

    print(f"\n[자동 코어] {route['model']} 실행 중 ...")
    full = run_model(cfg, route["model"], route["endpoint"], prompt, cfg["seed"])
    synthesis = extract_synthesis(full) or full[:300]
    m = int(has_marker(full)); rho = int(refuses_binary(synthesis))
    kop = round(k_op(synthesis), 2); nu = nu_against_pool(synthesis, cid)
    alpha_fires = (purpose == "synthesize" and kop <= cfg["alpha_kop_threshold"])
    trace.update({"m": m, "rho": rho, "nu": nu, "kop": kop, "alpha_fires": alpha_fires})
    print(f"지표: 마커={m} 이항거부={rho} 새로움(ν)={nu} 작동구조(κ)={kop}  -> 진정성 게이트 발동: {alpha_fires}")

    if alpha_fires:
        label = gate_alpha(cfg, synthesis, nu, kop, auto)
        trace["alpha_label"] = label
        if label == "C":
            rr = cfg["routing"]["alpha_cheat_reroute"]
            print(f"\n[판정=겉치레] 더 강한 모델로 재실행: {rr['model']} ({rr['endpoint']})")
            full = run_model(cfg, rr["model"], rr["endpoint"], prompt, cfg["seed"])
            synthesis = extract_synthesis(full) or full[:300]
            trace["rerouted"] = True; trace["reroute_model"] = rr["model"]
        elif label == "B":
            print("\n[판정=애매] 결정: a=이대로 수용, r=강한 모델로 재실행")
            if (ask("선택 [a/r, 기본 a]: ", "a") if not auto else "a") == "r":
                rr = cfg["routing"]["alpha_cheat_reroute"]
                full = run_model(cfg, rr["model"], rr["endpoint"], prompt, cfg["seed"])
                synthesis = extract_synthesis(full) or full[:300]
                trace["rerouted"] = True
            else:
                print("[수용]")
        else:
            print("[판정=진짜] 수용.")

    print("\n" + "=" * 64)
    print("최종 결과:")
    print("  " + synthesis.replace("\n", "\n  "))
    print("\n기록(TRACE):")
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
            print("목적을 고르세요:")
            print("  1) 결정            - 둘 중 하나를 골라야 할 때")
            print("  2) 종합            - 양쪽을 넘어선 제3의 안을 만들 때")
            print("  3) 전제 드러내기   - 숨은 가정을 찾아낼 때")
            pc = ask("선택 [1/2/3, 기본 2]: ", "2")
            purpose = PURPOSE_LABELS.get(pc, "synthesize")
            q_lines = paste_until_dot("질문을 붙여넣으세요 (여러 줄 가능; 마지막에 . 만 적힌 줄로 종료):")
            question = " ".join(l.strip() for l in q_lines if l.strip())
            if not question:
                print("질문이 필요합니다."); continue
            f_lines = paste_until_dot("사실을 붙여넣으세요 (한 줄당 한 사실; 마지막에 . 만 적힌 줄로 종료):")
            facts = [l.strip() for l in f_lines if l.strip()]
            if not facts:
                print("사실이 최소 1개 필요합니다."); continue
            r_override = None
            if purpose == "decide":
                contested = ask("이 결정은 의견이 갈리는(어느 쪽이 맞는지 열린) 결정인가요? [y/n, 기본 y]: ", "y")
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