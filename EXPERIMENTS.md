# 실험 순서 및 결과 맵 (Experiments Index)

이 리포는 "형식이 내용을 지배한다"는 명제를 LLM에서 시험하는 **두 실험**을 순차적으로 수행한다. 아래 맵으로 각 실험의 질문·설계·파일(설정·러너·분석·데이터·리포트)·재현 명령·핵심 결과를 구분할 수 있다.

| # | 실험 | 질문 | 설계 | 데이터 | 리포트 |
|---|---|---|---|---|---|
| **Exp 1** | 형식이 내용을 지배하는가 (단일 모델·8형식) | 같은 내용, 형식만 바꾸면 결론이 달라지는가? | 1모델 × 8형식 × 3항목 × 5반복 = **120** | `raw_runs.jsonl`·`analysis.json` | `REPORT.*`, `ITEMS.*` |
| **Exp 2** | Pruner MVP 다중 모델 | 목적→템플릿 바인딩이 모델 타입에 걸쳐 어떻게 달라지는가? | 8모델 × 3목적 × 2항목 × 2반복 = **96** | `mvp_runs.jsonl`·`mvp_analysis.json` | `MVP_STUDY.*` |

**순서·의존성**: Exp 1 → (Pruner MVP 타협점 승인) → Exp 2. Exp 2는 Exp 1의 forms/items를 재사용하고 Pruner의 선형 척춄를 검증한다.

---

## Exp 1 — 형식이 내용을 지배하는가 (단일 모델 · 8형식)

- **질문:** 같은 중립 사실과 같은 질문을 주고 **형식만 바꿀 때**, 산출물이 단지 화법이 아니라 *판정(verdict)*에서 달라지는가?
- **설계:** `gpt-oss:120b` 고정, 8개 형식(재배열 5 + 생성 3), 3개 통제 항목, 5회 반복 = **120 completions**. 측정: TF-IDF 표면 비율 + 스타일 제거 verdict 분산.
- **파일:**
  - 설정: `runner/config.json`
  - 러너: `runner/run_experiments.py` → `data/raw_runs.jsonl` (로그 `data/experiment.log`)
  - 분석: `analyze/analyze.py`, `analyze/extract.py` (결론 추출) → `data/analysis.json`
  - 리포트: `report/REPORT.ko.md` · `report/REPORT.md`, `report/ITEMS.ko.md` · `report/ITEMS.md`
- **재현:**
  ```bash
  source .venv/bin/activate && source .env
  ./run.sh experiments      # = python -m runner.run_experiments
  python -m analyze.analyze
  ```
- **핵심 결과:** TF-IDF 비율 1.19 (형식 효과 존재 but 노이즈 한계), **스타일 제거 verdict 분산 0.283 → 내용(판정) 수준에서 H1 성립**. 가장 쟁점적 항목(minimum_wage)에서 형식별 판정 갈림(0.425). 헤겔 triad는 이항을 거부하고 제3의 종합 생산(H1a).

## Exp 2 — Pruner MVP 다중 모델 (목적→템플릿 바인딩 × 8 모델 타입)

- **기원:** Pruner(MVP) 타협점 승인. $\Phi$(이상 템플릿 생성)은 블랙박스로 둔 채 선형 척춄(목적→바인딩→실행→인간 판정)을 다양한 모델에 시험.
- **질문:** 목적→템플릿 바인딩이 형식의 *구조*와 *판정*을 모델 타입에 걸쳐 어떻게 지배하는가?
- **설계:** 3 목적(`decide/synthesize/surface_assumptions`) → 바인딩(`red_blue_debate/dialectical_triad/socratic_dialogue`) × 2 항목 × 8 모델 타입 × 2반복 = **96 completions**.
- **파일:**
  - 설정: `runner/mvp_config.json`
  - 러너: `runner/run_mvp.py` → `data/mvp_runs.jsonl` (로그 `data/mvp_run.log`)
  - 분석: `analyze/analyze_mvp.py` → `data/mvp_analysis.json`
  - 리포트: `report/MVP_STUDY.ko.md` · `report/MVP_STUDY.md`
- **재현:**
  ```bash
  source .venv/bin/activate && source .env
  python -m runner.run_mvp
  python -m analyze.analyze_mvp
  ```
- **핵심 결과:** (1) 형식의 **구조** 지배는 모델 무관(마커 실현률 ~1.0, general-moe만 0.75–0.875). (2) 형식의 **판정** 지배는 모델 의존적 — `minimum_wage/decide`에서 같은 형식 하에 support/oppose로 갈림 → $\Phi$가 블랙박스인 것이 정당화. (3) **Aufheigung(triad 종합)**은 모든 모델 타입에서 재현(novelty 0.71–0.89, H1a robust).

## 공유 인프라 (두 실험 공통)
- `runner/forms.py` — 8개 형식 템플릿 라이브러리 + family 분류
- `runner/llm.py` — Ollama Cloud(OpenAI 호환) 클라이언트 (`chat` + 메타 반환 `chat_meta`)
- `content/dataset.json` — 3개 통제 콘텐츠 항목(중립 사실 + 쟁점 질문)
- `forms/` — 형식 템플릿(철학 주석 포함)

## 디렉토리 → 실험 매핑
```
runner/
  config.json          ── Exp 1 설정
  run_experiments.py   ── Exp 1 러너
  mvp_config.json      ── Exp 2 설정
  run_mvp.py           ── Exp 2 러너
  forms.py / llm.py    ── 공유
analyze/
  extract.py / analyze.py    ── Exp 1 분석
  analyze_mvp.py             ── Exp 2 분석
data/ (git 제외, analysis.json/mvp_analysis.json은 커밋)
  raw_runs.jsonl + analysis.json      ── Exp 1
  mvp_runs.jsonl + mvp_analysis.json  ── Exp 2
report/
  REPORT.* / ITEMS.*        ── Exp 1
  MVP_STUDY.*               ── Exp 2
```