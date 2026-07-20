# 형식이 내용을 지배한다 — LLM 안에서의 경험적 검증

> *"Die Form regiert den Inhalt." — 형식이 내용을 지배한다.* (헤겔)

헤겔의 명제를 LLM 안에서 경험적으로 시험한 파일럿 연구입니다. **같은 중립 사실과 같은 질문**을 주고 **형식만 바꿨을 때**, 모델의 산출물이 단지 화법만 바뀌는 게 아니라 **실질적 내용(판정·결론)이 달라지는가?**

* 📖 **상세 리포트**: [`report/REPORT.ko.md`](report/REPORT.ko.md) (한국어) · [`report/REPORT.md`](report/REPORT.md) (English)
* 📑 **항목별 상세 설명**: [`report/ITEMS.ko.md`](report/ITEMS.ko.md) (한국어) · [`report/ITEMS.md`](report/ITEMS.md) (English)
* 🌐 **English version of this README**: [`README.en.md`](README.en.md)
* 🧪 **MVP 다중모델 연구**: [`report/MVP_STUDY.ko.md`](report/MVP_STUDY.ko.md) (한국어) · [`report/MVP_STUDY.md`](report/MVP_STUDY.md) (English)
* 🔍 **Exp 3 로컬 triad 검증**: [`report/EXP3_STUDY.ko.md`](report/EXP3_STUDY.ko.md) (한국어) · [`report/EXP3_STUDY.md`](report/EXP3_STUDY.md) (English)
* 🎛️ **정합 뷰(v0.3.0 제어판)**: [`report/CONTROL_PANEL.md`](report/CONTROL_PANEL.md) (한국어) · [`report/CONTROL_PANEL.en.md`](report/CONTROL_PANEL.en.md) (English)
📐 **제어판 설계 명문**: [`report/CONTROL_PANEL_SPEC.md`](report/CONTROL_PANEL_SPEC.md) (한국어) · [`report/CONTROL_PANEL_SPEC.en.md`](report/CONTROL_PANEL_SPEC.en.md) (English)

---

## 1. 가설

| 번호 | 가설 | 내용 |
|---|---|---|
| **H1** (헤겔, 강) | 형식은 불활성 그릇이 아니라 내용이 *무엇이 되는지*를 결정한다. 따라서 원-내용·모델·시드·온도를 고정하고 형식만 바꾸면, *추출된 결론*이 형식 간에 형식 내 반복보다 더 많이 갈린다. |
| **H1a** (헤겔, 변증법) | 내용을 모순을 통해 *발전*시키도록 강제하는 생성형 형식(변증법 triad·소크라테스 대화·찬반 토론)은, 재배열형 형식(불릿·JSON·삼단논법)보다 더 많은 새 명제와 더 단호한/다른 결론을 생산한다. 특히 **정-반-합 triad**는 이항 대립을 거부하고 *제3의 종합적 판정*을 만들어낸다. |
| **H0** (스타일 전용) | 형식은 표면 스타일만 바꿀 뿐, 추출된 결론은 형식과 무관하게 수렴한다. (LLM에서 헤겔 거짓) |

## 2. 증명(실험) 과정

### 설계 — 한 축은 고정, 한 축은 변화
| 축 | 고정(내용) | 변화(형식) |
|---|---|---|
| 원-내용(중립 사실 + 쟁점 질문) | ✔ (3개 항목) | |
| 프롬프트 형식 | | ✔ (8개 템플릿, 2개 계열) |
| 모델·온도·시드·반복 | ✔ (gpt-oss:120b, T=0.3, seed 42–46, 5회 반복) | |

- **3개 통제 항목**: `battery_limits`(기술 정책), `minimum_wage`(경제학), `pluto_planet`(과학 분류). 각 항목은 양쪽 모두를 지지하는 사실들로 구성해 형식이 판정을 좌우할 여지를 둠. *항목별 상세 설명은 [`report/ITEMS.ko.md`](report/ITEMS.ko.md) 참고.*
- **8개 형식, 2개 계열**:
  - 재배열형 5개 — `bullet_list`, `numbered_steps`, `json_schema`, `qa_pairs`, `syllogism` (내용을 재배열)
  - 생성형 3개 — `dialectical_triad`(정-반-합), `socratic_dialogue`, `red_blue_debate` (내용을 모순을 통해 발전)
- **24셀 × 5반복 = 120회 호출**. Ollama Cloud의 `gpt-oss:120b` 사용.
- 각 산출물에서 결론 문장을 추출해 스타일을 제거한 뒤 두 가지로 측정.

### 두 가지 측정 — "형식이 내용을 지배한다"를 스타일 효과와 구별
핵심은 **결론(판정)만 비교**해 화장술 효과와 실질 내용 효과를 분리하는 것.

1. **TF-IDF 표면 비율** = (형식 간 코사인 거리) ÷ (형식 내 코사인 거리). `≫1`이면 형식이 내용 지배(H1), `≈1`이면 형식은 화장술(H0).
2. **verdict 분산(스타일 제거)**: 결론을 항목별 stance 라벨(`support`/`oppose`/`qualified` 등)으로 분류한 뒤, 같은 내용에서 형식만 바꿨을 때 판정이 갈리는 비율 = `1 − (최대 라벨 점유율)`. 높으면 형식이 *판정*을 좌우 → 형식이 내용 지배.

## 3. 결론

### 핵심 수치 (`data/analysis.json`)
| 측정 | 값 | 해석 |
|---|---|---|
| TF-IDF 표면 비율 (across/within) | **1.19** | >1 (형식 효과 존재)이지만 엄격 기준(1.5) 미만. reasoning 모델의 표면 분산이 within 분모를 부풀려 과소평가. |
| within-form 분산 (재배열 / 생성) | 0.73 / 0.85 | 생성형이 같은 형식 반복에서도 표면이 더 다양 — "발전"하는 형식의 특성. |
| **verdict 분산(스타일 제거), 전체** | **0.283** | 같은 내용에서 형식만 바꿨을 때 판정이 갈리는 비율. |
| `hegel_h1_verdict` (분산 > 0.15) | **true** | **내용(판정) 수준에서 H1 성립.** |

### 가장 강력한 신호: minimum_wage (verdict 분산 0.425)
같은 중립 사실, 형식만 바꿨을 때 **판정이 갈림**:
- `socratic_dialogue` / `red_blue_debate` → **"지지"** 5/5 (단호한 찬성)
- `bullet_list` / `syllogism` / `dialectical_triad` → **"qualified"** (신중·조건부)
- `json_schema` → **"oppose"로 기울기** (유일하게 부정 쪽 분기)

### 헤겔 변증법 triad의 정확한 예측 (H1a)
`dialectical_triad`는 minimum_wage에서 **5/5 "qualified"** — 극 중 하나를 고르지 않고 *인플레이션 연동·지역별 조정·안전장치*라는 제3의 종합적 판정(Aufhebung)을 만들어냄. 이것이 헤겔 예측 그대로: triad는 내용을 "재배열"한 게 아니라 **다른 종류의 내용을 생산**함.

### 형식 유형별 "특성 내용"
- **대화/대립형 생성 폼** → 더 단호한 판정에 커밋
- **구조적/분석적 재배열 폼** → "qualified"로 헤징
- **경직된 JSON 폼** → 유일하게 부정 쪽으로 넛징
- pluto_planet에서 `red_blue_debate`만 "왜소행성 유지"로 보수적 판정(판사 형식의 기본 성향)

### 결론
**동일한 사실과 동일한 질문에서 형식만 바꿔도 모델의 대답이 달라진다 — 단지 화법이 아니라 판정 자체가.** 표면(TF-IDF) 측정은 reasoning 모델의 노이즈에 묻혀 약하지만, 스타일을 제거한 verdict 측정은 ~28%(가장 쟁점적인 항목에서는 ~43%)의 분기를 보여준다. **형식은 엔지니어링 폴리시가 아니라 결과의 결정적 일부**다. 헤겔의 명제가 LLM 안에서 실질적으로(스타일이 아닌 내용 수준에서) 재현되었다.

> 한계: n=3항목 × 5반복 파일럿 · verdict 분류는 항목별 키워드 휴리스틱 · TF-IDF는 스타일 누출. LLM-judge 기반 verdict 추출과 sentence-embedding 도입이 자연스러운 다음 단계. 상세한 한계와 확장 계획은 상세 리포트 참고.

## 리포지토리 구조
```
form-governs-content/
├── README.md               이 파일 (한국어 연구 개요)
├── README.en.md            English overview
├── EXPERIMENTS.md          실험 순서·결과 맵 (한) / .en.md (영)
├── run.sh                  .env 로드 + venv 활성화 + 파이프라인 실행
├── requirements.txt
├── .env                    OLLAMA_API_KEY + VENV_ACTIVATE (git 제외)
├── forms/                  8개 형식 템플릿 (철학 주석 포함)
├── content/dataset.json    3개 통제 콘텐츠 (중립 사실 + 쟁점 질문)
│   └── exp3_items.json     Exp3 개방형 설계 2개
├── runner/                 config.json / mvp_config.json / exp3_config.json
│   └── forms.py / llm.py / run_experiments.py / run_mvp.py / run_exp3.py
├── analyze/                extract.py / analyze.py / analyze_mvp.py
│   └── analyze_exp3.py / analyze_alpha.py / analyze_alpha_stageB.py
├── report/                 REPORT·ITEMS·MVP_STUDY·EXP3_STUDY·ROUTING (한/영)
│   └── CONTROL_PANEL(+SPEC)·PRUNER_LOG·ALPHA_LABELS_SHEET
└── data/                   raw_runs/mvp_runs/exp3_runs.jsonl + *_analysis.json + alpha_dissolution_stageA/B.json (커밋됨; *.log만 제외)
```

## 재현
```bash
cp .env.example .env        # OLLAMA_API_KEY 와 VENV_ACTIVATE 입력
./run.sh experiments        # Exp1: 120 호출 → data/raw_runs.jsonl
python -m runner.run_mvp    # Exp2: 96 호출 (8 클라우드 모델)
python -m runner.run_exp3   # Exp3: 75 호출 (5 로컬 모델, 1–12B)
python -m analyze.analyze        # Exp1 메트릭
python -m analyze.analyze_mvp    # Exp2 메트릭
python -m analyze.analyze_exp3   # Exp3 크로스-모델
python -m analyze.analyze_alpha        # α Stage A (관측량)
python -m analyze.analyze_alpha_stageB  # α Stage B (인간 라벨→소멸 잔여)
```
설정: 각 `runner/*.json`. 환경: `python-dotenv`, `requests`, `numpy`, `scikit-learn`.

## 프로젝트 최종 상태 (v0.3.0) — 종료 조건 도달
- **총 291 completions**: Exp1(120) · Exp2(96) · Exp3(75).
- **결과 계보**: 형식이 내용을 지배(Exp1) → 창의성은 형식에서·1B 비-reasoning까지 robust(Exp3) → 모델 선택은 대부분 자동 코어로 소멸, decide 쟁점만 `intent`로 실재(Exp2) → α(진정성)는 소멸 저항으로 실재(Stage A/B) → **완전 자동 $I_0$ 는 환상 확정**.
- **발견된 제어판**: 자동 코어 + {`intent`, α} 2-컨트롤. 두 컨트롤 모두 소멸 저항(실재) → 더 삭제할 환상 컨트롤 없음 → 제어판 안정 = 산출물. 상세: [`report/CONTROL_PANEL.md`](report/CONTROL_PANEL.md) · 설계: [`report/CONTROL_PANEL_SPEC.md`](report/CONTROL_PANEL_SPEC.md).
- **방법론 산출물**: 본 연구를 수행한 Pruner 스킬 `pruner-arch` v0.3.0([github.com/sng2c/pruner-arch](https://github.com/sng2c/pruner-arch)) — 정합적 이상·프랙탈 분해·환상 컨트롤 삭제·제어판 발견. 스킬이 스스로를 검증한 형태.
