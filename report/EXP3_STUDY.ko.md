# Exp 3 — 로컬 소형 모델에서 변증법 triad의 창의적 종합(Aufhebung) 검증

> 영문 버전: [`EXP3_STUDY.md`](EXP3_STUDY.md) · 실험 인덱스: [`../EXPERIMENTS.md`](../EXPERIMENTS.md)

## 동기
Exp 2에서 cloud `gemma4:31b`이 triad 하에서 gpt-oss:120b와 질적으로 동등한 종합을 산출(novelty 0.764)하는 것을 관측. **"창의적 형식(triad)의 종합력이 모델 스케일/타입에 robust하면, 비싼 클라우드 reasoning 모델 없이도 로컬 소형 LLM으로 창의적 문제해결이 가능하지 않은가?"** 라는 가설(H_local)을 로컬에서 직접 검증.

## 가설 (H_local)
> 변증법 triad 형식의 Aufhebung(이항 거부 → 제3의 종합 생성)은 모델 스케일/타입에 robust하여, **소형 로컬 모델(12B MLX)에서도 창의적 문제해결(제3의 설계 산출)이 가능**하다.

## 설계
- **형식 고정**: `dialectical_triad` 단일 (창의성의 원천 = 형식).
- **로컬 모델**: `gemma4:12b-mlx`(7.7GB, MLX 가속, reasoning 모델) — 로컬 Ollama `localhost:11434`.
- **콘텐츠 5개**: 기존 3개 쟁점 항목 + **개방형 설계 2개**(`freshwater_alloc`, `density_greenspace` — 단일 정답 없음, 진짜 제3의 설계 강제).
- **3반복**, 동일 시드·온도·max_tokens. **15 로컬 호출**(무료, 평균 ~6분/항목).
- **측정**: `SYNTHESIS CONCLUSION` 마커, 이항 거부, 제3-명제 키워드, 항목 내 novelty(창의적 분산). **핵심 = 인간 $J$**: 종합 문장이 진짜 "양극의 단순 합이 아닌 제3의 명제"인지 정성 판정.

## 결과 (`data/exp3_analysis.json`)

### 정량 — 로컬 12B에서 Aufhebung이 100% 재현
| 항목 | 마커 | 이항거부 | 제3-키워드 | novelty |
|---|---|---|---|---|
| battery_limits (쟁점) | 1.0 | 1.0 | 0.33 | 1.0 |
| minimum_wage (쟁점) | 1.0 | 1.0 | 0.0 | 0.94 |
| pluto_planet (쟁점) | 1.0 | 1.0 | 0.67 | 1.0 |
| freshwater_alloc (**개방**) | 1.0 | 1.0 | 0.33 | 0.953 |
| density_greenspace (**개방**) | 1.0 | 1.0 | 0.33 | 1.0 |
| **전체** | **1.0** | **1.0** | 0.33 | **0.979** |

→ 로컬 12B 모델이 15회 전부 `SYNTHESIS CONCLUSION` 마커를 내고(1.0), 이항(yes/no)을 전부 거부(1.0). novelty(항목 내 3반복 간 분산) 0.94–1.0 → **같은 항목에서도 매번 *다른* 종합을 산출** = 창의적 분산이 매우 높음.

### 정성 — 인간 $J$: 진짜 제3의 명제인가? (이것이 핵심 증거)

**개방형 설계** (단일 정답 없음 — 창의성의 진짜 시험):

**freshwater_alloc** — 로컬 12B가 3개의 *서로 다른* 제3의 설계 산출:
- r0: *"정적 할당 모델에서 동적 계층 시스템으로 전환 — 기본 인간·생태 필요는 비협상 가능한 바닥으로 보장하고, 이후 사용은 'Net-Zero Extraction' 의무로 통제"*
- r1: *"실시간 희소 지수에 기반한 동적 가치밀도 할당 — 사회경제적 효용으로 분배하되 지하수 생태 한계 엄수"*
- r2: *"기본 필요는 공공재로 보장, 잉여 물은 산업용 거래 — 단 의무 재활용 할당으로 총 가용량을 확장하는 조건부"*

→ 각각이 양극(농업 vs 공업 vs 도시)의 단순 선택이 아니라 *제3의 제도 설계*(동적 바닥 / 실시간 지수 / 조건부 거래). **3회가 3개의 다른 창의적 설계** — novelty 0.953.

**density_greenspace** — 로컬 12B가 밀도 vs 녹지의 이항을 매번 다르게 지양:
- r0: *"집적 도시주의(Aggregated Urbanism) — 고밀도 용도를 도시스프롤의 파괴로부터 대규모 생태를 보존하는 전략적 방패로 사용"*
- r1: *"'생태적 밀도' — 녹지를 주거와 경쟁하는 선택적 편의가 아니라 의무적 공공 인프라로 법제화"*
- r2: *"녹지를 고밀도 거주의 생물학적 전제조건인 비협상적 공공 유틸리티로 취급"*

→ 밀도 vs 녹지를 "둘 중 하나"로 풀지 않고, 매번 *밀도를 녹지 보존의 수단으로 재정의*하는 제3의 프레이밍.

**쟁점 항목** (cloud 기준선과 비교 가능):
- **pluto_planet** r1: *"명왕성이 행성인가는 범주 오류; 정적 정의 대신 시스템적 지배도에 기반한 동적 분류로 대체"* — **문제 자체를 격상**(이항 거부 + 분류 체계 재설계). gpt-oss:120b의 "이중기준 정의"와 동등한 수준의 창의적 지양.
- **battery_limits** r1: *"단일 마일스톤 조건을 '동적 기술준비도 프레임워크'로 교체"* — cloud triad의 "자동차 특화 마일스톤" 재지정과 동일 패턴.

## 해석 — H_local 지지
1. **창의성의 원천은 형식, 모델이 아니다.** 로컬 12B reasoning 모델이 triad 형식 하에서 cloud 120B와 *질적으로 동등한* Aufhebung(이항 거부 + 제3의 설계 산출)을 100% 재현. 창의적 종합력은 모델 용량이 아니라 **변증법 형식이 강제하는 구조적 운동**에서 옴.
2. **로컬 LLM 창의적 문제해결 가능.** 개방형 설계(단일 정답 없음)에서조차 매번 *다른* 제3의 설계를 산출(novelty 0.94–1.0). 비싼 클라우드 대형 모델 없이 로컬 소형 모델 + triad 형식으로 창의적 문제해결이 실용적으로 가능.
3. **라우팅 MVP의 `synthesize→최저비용` 레그가 로컬까지 안전.** Exp 2(cloud 31B) + Exp 3(로컬 12B) 모두에서 triad의 종합력 robust → 종합 목적엔 로컬 소형 모델 배정 가능(비용 0, 지연만).
4. **novelty 0.94–1.0의 의미**: 같은 항목·같은 형식·같은 시드 오프셋인데도 매번 다른 종합 → triad는 *결정론적 답*이 아니라 *창의적 분산*을 발생시키는 형식. 이것이 "형식이 내용을 생산한다"는 헤겔 명제의 가장 강한 실증.

## ⚑ Exp 3b — 비-reasoning 소형 모델 확장 (옵션 B 수행)
`gemma4:12b-mlx`가 reasoning 모델이었으므로, "Aufhebung이 *reasoning 능력*이 아니라 *형식*에서 오는가?"를 검증하기 위해 **비-reasoning 소형 모델** 2종을 추가 시행(llama3.2:3b·gemma3:4b, triad 고정, 동일 5항목 × 3반복 = 30 로컬 호출).

### 크로스-모델 정량
| 모델 | 종류 | 마커 | 이항거부 | 제3-키워드 | novelty |
|---|---|---|---|---|---|
| gemma4:12b-mlx | reasoning | 1.0 | 1.0 | 0.4 | 0.979 |
| **gemma3:4b** | **비-reasoning** | **1.0** | **1.0** | 0.33 | 0.965 |
| **llama3.2:3b** | **비-reasoning** | **0.8** | **1.0** | 0.27 | 0.983 |

### 핵심 발견 — reasoning 없이도 Aufhebung 재현
1. **이항 거부 = 1.0 이 세 모델 전부**(reasoning·비-reasoning·3B 소형). → triad의 핵심 Aufhebung 속성(이항 거부)은 **reasoning 능력이 아닌 형식에서 온다**. 3B 비-reasoning 모델조차 이항(yes/no)을 전부 거부.
2. **novelty 0.96–0.98 전부** — 창의적 분산도 reasoning 무관. 3B 비-reasoning도 매번 *다른* 종합 산출(0.983).
3. **형식 *준수*(마커 방출)는 용량 민감**: gemma4(12B reasoning)·gemma3(4B 비-reasoning)는 마커 1.0이나, **llama3.2:3b는 0.8**(간혹 `**THESIS` 원 템플릿 누출로 마커 누락). → *구조 준수*는 용량에 민감하지만, *변증법 운동*(이항 거부 + 제3 설계)은 형식 주도로 robust.
4. **정성(인간 J)** — 4B 비-reasoning(gemma3:4b)이 진짜 제3의 설계 산출: freshwater "계층 시스템 + 전용 backstop 기금", pluto **"주왕성(major dwarf planet)"이라는 제3 범주**(planet/dwarf 이항 거부 + 새 범주 생성), density "밀도+생태 공공공간 통합 레이어드 접근". 3B(llama3.2:3b)도 minimum_wage "인플레이션 연동·부문별 index + caution" 같은 제3 설계 산출(단 마커 누락 잦음).

→ **H_local 강화**: 창의성의 원천은 형식이지 reasoning이 아니다. 비-reasoning 4B에서 Aufhebung이 *완전히*(마커 1.0) 재현되고, 3B에서도 *내용적으로* 재현(마커 0.8이나 이항거부 1.0·novelty 0.98). **로컬 비-reasoning 소형 모델(3–4B)만으로 triad 기반 창의적 문제해결 실용 가능** — reasoning 단계·대형 모델 불필요.

## ⚑ Exp 3c — 극소형 1B 비-reasoning 모델 (옵션 C)
옵션 B가 비-reasoning 3–4B까지 잡았으므로, 마지노선을 보기 위해 **1B급 극소형 비-reasoning** 2종(`llama3.2:1b`, `gemma3:1b`)을 추가 시행(triad 고정, 동일 5항목 × 3반복 = 30 로컬 호출).

### 5-모델 크로스 정량 (총 75 runs)
| 모델 | 종류 | 마커 | 이항거부 | 제3-키워드 | novelty |
|---|---|---|---|---|---|
| gemma4:12b-mlx | reasoning | 1.0 | 1.0 | 0.4 | 0.979 |
| gemma3:4b | 비-reasoning | 1.0 | 1.0 | 0.33 | 0.965 |
| **gemma3:1b** | **비-reasoning 1B** | **1.0** | **1.0** | **0.73** | **0.995** |
| llama3.2:3b | 비-reasoning | 0.8 | 1.0 | 0.27 | 0.983 |
| **llama3.2:1b** | **비-reasoning 1B** | **0.933** | **1.0** | **0.73** | 0.958 |

### 핵심 — 1B에서도 Aufhebung 재현 (가장 강한 H_local 증거)
1. **이항 거부 = 1.0, 두 1B 모델 모두**. 1B 비-reasoning조차 매번 yes/no를 거부. → Aufhebung의 핵심은 *reasoning도 용량도 아닌 형식*에서.
2. **마커 준수**: `gemma3:1b`가 **1.0**(1B인데 3B llama보다 *나음*), `llama3.2:1b` 0.933(15회 중 1회만 마커 누락). → **형식 준수는 크기 단조가 아니다**: Gemma 계열이 Llama보다 동일 크기에서 형식을 더 잘 따름. 가족·양자화 의존.
3. **novelty 0.958–0.995 at 1B** — 창의적 분산이 1B에서도 유지. 매번 *다른* 종합.
4. **제3-키워드 0.73 (1B)** — 3–4B(0.27–0.33)보다 *높음*. 소형 모델이 템플릿의 “not X but Y / reframe / shift” 구문에 더 강하게 기대는 경향(형식 의존도가 오히려 증가).
5. **정성(인간 J)** — 1B가 *명명된* 제3 시스템 산출: `gemma3:1b` freshwater **“Dynamic Adaptive Allocation System — 참여적·생태-정보화·사회정의”**, density **“정치 동원(공원 보존)과 생태 재생(녹지 창출)이 상호 강화되는 변증법적 과정”**(명시적 변증법!), pluto “동적 궤도 안정성·활성 지질·자가지속 형성 우선의 개정 정의”. `llama3.2:1b` freshwater **“Water Stewardship Model”**, pluto “궤도 경로 명확성과 중력 상호작용의 가능성을 균형잡는 개정 정의로 명왕성 지위 격상”.

→ **H_local 최종 지지**: **1B 비-reasoning 극소형 모델에서도 triad의 Aufhebung이 재현**(이항거부 1.0, 마커 0.93–1.0, novelty 0.96–0.995, 명명된 제3 설계 산출). **로컬 극소형 LLM(1B, 비-reasoning)만으로 triad 형식 기반 창의적 문제해결이 실용 가능** — reasoning·대형 모델·클라우드 전부 불필요. 창의성은 모델 용량이 아니라 변증법 형식의 구조적 운동에서 비롯된다.

## 한계 / 다음 단계
- **1개 로컬 모델**(`gemma4:12b-mlx`)만. 주장을 단단히 하려면 비-reasoning 소형 모델(`qwen3:8b`, `llama3.2:3b`)까지 확장해 "reasoning 아닌 소형 모델에서도 Aufhebung 재현?" 검증. (사용자 옵션 B 후보)
- **정성 $J$는 저자 단독**. 독립 인간 판정/LLM-judge로 "제3의 명제" 품질 교차검증 필요.
- **개방형 항목 2개**. 설계 과제 풀 확장 시 창의성 범위 더 측정.
- **이항거부 1.0 / 마커 1.0**은 형식 *준수*이지 종합 *품질*이 아님 — third_word_count(0.33)는 보수적이므로, 정성 $J$가 더 신뢰.

## 재현
```bash
source .venv/bin/activate && source .env
python -m runner.run_exp3        # 15 로컬 호출 → data/exp3_runs.jsonl
python -m analyze.analyze_exp3   # → data/exp3_analysis.json + 종합 문장 출력
```
설정: `runner/exp3_config.json` · 콘텐츠: `content/exp3_items.json`(개방형 2개) + `content/dataset.json`(기존 3개).