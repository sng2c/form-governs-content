# MVP 연구 — 다양한 모델 타입에 걸친 목적→템플릿 바인딩 시행

> 영문 버전: [`MVP_STUDY.md`](MVP_STUDY.md) · 주 리포트: [`REPORT.ko.md`](REPORT.ko.md)

Pruner(MVP) 타협점 승인 후 진행한 후속 실험. **$\\Phi$(이상 템플릿 생성)는 블랙박스로 둔 채**, 선형 척춄(목적→바인딩→실행)을 Ollama Cloud의 **8개 모델 타입**에 걸쳐 시행하고, "형식이 내용을 지배한다"는 모델 의존적으로 어떻게 변하는지 분석.

## 설계 (MVP 선형 척추)
$$P \\xrightarrow{\\text{바인딩}} T_k \\xrightarrow{M} O \\xrightarrow{\\text{인간 } J}$$
- 목적 $P \\in \\{$`decide`, `synthesize`, `surface_assumptions`$\\}$ (Pruner 분류체 $\\Pi$의 부분집합).
- 바인딩 $\\Pi\\to\\mathcal{T}$: `decide→red_blue_debate`, `synthesize→dialectical_triad`, `surface_assumptions→socratic_dialogue`.
- 콘텐츠 2개: `minimum_wage`(가장 쟁점적), `pluto_planet`(비교적 명확).
- 8개 모델 타입(2반복): `gpt-oss:120b`·`deepseek-v4-flash`(reasoning) / `kimi-k2.6`·`qwen3.5:397b`(general-moe) / `mistral-large-3:675b`(large-dense) / `glm-5.2`·`minimax-m3`(general) / `gemma4:31b`(small-efficient).
- **96 completions** (8모델 × 3목적 × 2콘텐츠 × 2반복), 동일 시드·온도·max_tokens.

## 핵심 결과 (`data/mvp_analysis.json`)

### 1. 형식의 *구조* 지배는 모델 타입에 걸쳐 robust하다
필수 마커(`DEBATE/SYNTHESIS/DIALOGUE CONCLUSION`) 존재 비율(목적 실현률):
| 모델 타입 | decide | synthesize | surface_assumptions |
|---|---|---|---|
| reasoning | 1.0 | 1.0 | 1.0 |
| general-moe | 0.75 | 0.875 | 1.0 |
| large-dense | 1.0 | 1.0 | 1.0 |
| general | 1.0 | 1.0 | 1.0 |
| small-efficient | 1.0 | 1.0 | 1.0 |

→ MVP의 **선형 척춄은 모델 타입에 robust**: 거의 모든 모델이 변증법 형식의 구조적 요구(마커·섹션)를 따른다. general-moe(kimi/qwen)만 간혹 마커 누락(0.75/0.875). 즉 "형식이 구조를 지배한다"는 모델에 크게 의존하지 않는다.

### 2. 하지만 형식의 *판정(verdict)* 지배는 모델 의존적이다
**`minimum_wage / decide` (red_blue_debate)** 에서 *같은 형식* 하에 모델이 갈린다
(2회 시행의 stance 분포, `data/mvp_analysis.json`의 `decide_stance_by_model` 기준 —
`analyze_mvp.py`의 키워드 stance 휴리스틱 결과로 정성 $J$ 재검증 필요):

| 모델 | 2회 stance 분포 | 요약 |
|---|---|---|
| **gemma4:31b** | **yes 2 · qualified 0 · no 0** | **단호 지지 (유일)** |
| deepseek-v4-flash | qualified 2 | 유보 |
| minimax-m3 | qualified 2 | 유보 |
| mistral-large-3:675b | qualified 2 | 유보 |
| gpt-oss:120b | yes 1 · qualified 1 | 혼합 |
| kimi-k2.6 | yes 1 · qualified 1 | 혼합 |
| qwen3.5:397b | yes 1 · qualified 1 | 혼합 |
| glm-5.2 | yes 1 · qualified 1 | 혼합 |

→ **같은 쟁점적 내용·같은 red/blue 형식에서 모델에 따라 판정이 갈린다**:
**단호한 "yes(지지)" 2/2는 small-efficient `gemma4:31b` 단독**이고, reasoning 여부와 무관하게
나머지 7개 모델은 모두 `qualified`(유보)를 1회 이상 포함. (이전 버전은 이 표를 support/oppose
4:4 분할로 기술했으나, 이는 구 stance 휴리스틱 결과로 `mvp_analysis.json`과 정합하지 않다 —
위 표가 데이터 기준 정본.) 핵심 결론은 동일: 같은 형식이라도 *판정*은 모델 의존적으로
갈린다 → $\Phi$가 블랙박스로 남은 것이 정당화됨. 반면 명확한 항목 `pluto_planet`에서는
7/8 모델이 "재분류(yes) 2/2"로 수렴(mistral만 yes 1 + qualified 1).

⇒ **형식은 구조를 모델 무관하게 지배하지만, 판정은 쟁점적 항목에서 모델 의존적**. 이것이 바로 $\\Phi$가 블랙박스로 남은 이유: 단일 바인딩된 템플릿은 모든 모델에서 *올바른* 판정을 보장하지 못한다. **인간 $J$ 게이트가 쟁점적 항목에서 여전히 필요**하다.

### 3. Aufhebung(종합)은 모든 모델 타입에서 재현된다 (H1a)
`synthesize / dialectical_triad`의 새 명제 생성률(**cross-model novelty** — 해당 모델 결론이 *다른 7개 모델 결론* 대비 갖는 shingle 신규성):

> ⚠️ **novelty 정의 주의**: 본 절의 `synth_novelty`는 **cross-model**(타 모델 대비 독창성)이다.
> Exp 3의 `within_item_novelty`(**같은 모델·같은 항목 3반복 간 분산**)과 **정의가 달라 직접 비교 불가**.
> 예컨대 Exp3 `gemma3:1b`의 0.995(반복마다 매번 다른 추상 표현)를 본 절의 0.894(타 모델 대비
> 독창성)와 같은 축에 올려 "로컬 1B가 클라우드 120B보다 창의적"이라 비교하면 안 된다 — 오히려
> cross-model 기준에서는 `gemma4:31b`=0.764로 본 표 최하위다.
| 모델 | novelty | 결론 예 |
|---|---|---|
| gpt-oss:120b | **0.894** | "동적 인덱싱·지역 차등 최저임금 + 표적 보조금·EITC 확대로 빈곤 탈출" |
| kimi-k2.6 | 0.889 | (양극을 지양한 동적 시스템) |
| minimax-m3 | 0.88 | "고정 인상이 아니라 인덱싱·지역 보정 재설계 지지" |
| mistral-large-3 | 0.86 | "지역 차등·인플레이션 연동·고용 리스크 완화 정책과 병행할 때만 정당" |
| qwen3.5:397b | 0.796 | (종합 산출, 단 마커 누락 경향) |
| deepseek-v4-flash | 0.768 | "인덱싱·지역 차등 기제로만 인상 지지" |
| gemma4:31b | 0.764 | "일회성 명목 인상이 아니라 동적·인덱싱 시스템으로 전환" |
| glm-5.2 | 0.713 | (가장 보수적이나 여전히 종합적) |

→ **triad 형식의 핵심 속성(이항 거부 + 제3의 종합 생산)은 모든 모델 타입에서 재현** (0.71–0.89). 가장 작은 비-사고 모델(gemma4:31b)조차 triad 하에서는 단순 찬/반 대신 "동적·인덱싱 시스템으로의 전환"이라는 종합을 산출. 헤겔 H1a가 모델 타입에 걸쳐 robust.

### 4. 사고(reasoning) 여부와 장황함
- 사고 모델(gpt-oss/deepseek/glm/kimi/minimax/qwen)과 비사고 모델(gemma4:31b, mistral-large-3:675b) 모두 형식을 따름.
- 가장 장황: kimi-k2.6(10,016자) · 가장 간결: gemma4:31b(2,695자).
- 주의: 비사고 소형 모델 gemma는 `decide`에서 가장 단호한 "yes(지지)" 2/2를 내며, reasoning 모델들이 `qualified`로 유보하는 것과 대조적으로 단순 이항에 더 쉽게 커밋 — **reasoning 단계가 없을수록 형식의 이항 구조(red/blue)에 더 그대로 노출**되어 확정 stance를 찍는 경향. 단, 이 "단호함"은 `analyze_mvp.py`의 키워드 stance 휴리스틱에 의존하므로 정성 $J$ 재검증이 필요하다.

## 해석 — MVP 설계 베팅의 검증
1. **선형 척춄은 성립**: 목적→바인딩→실행은 8개 모델 타입 전부에서 안정적으로 형식의 *구조*를 실현(마커 1.0에 가까움).
2. **비선형 $\\Phi$는 블랙박스로 였던 것이 정당화됨**: 같은 형식이라도 *판정*은 쟁점적 항목에서 모델 의존적으로 갈림. 즉 "목적에 대한 이상 템플릿"은 모델까지 고려해야 비로소 정의되므로, 단일 바인딩으로는 불충분 — 이것이 $\\Phi$가 비선형인 이유.
3. **Aufhebung은 형식의 모델 무관 속성**: triad의 "이항 거부→제3 종합"은 모델 타입에 robust → 형식 중에서도 *생성형* 변증법 형식이 내용을 지배하는 힘은 모델 의존적이지 않다.
4. **인간 $J$ 게이트의 역할 확인**: 쟁점적 항목에서 모델 간 판정 분기가 발생하므로, MVP는 "판정"을 자동화하지 않고 인간 게이트에 둔 설계가 맞았다.

## 한계 / 다음 단계 (Pruner 하강 후보)
- 3 목적 × 2 콘텐츠 × 2반복 파일럿. $\\Pi$ 전체(6목적)·콘텐츠 확장·반복 증가 필요.
- 자동 $J$ 프록시(마커/stance/신규성)는 휴리스틱; LLM-judge 도입 시 판정-정확도 측정 가능.
- $\\Phi$ 블랙박스를 여는 하강 = "목적으로부터 *생성*하는* 템플릿"($I_1$) 설계 — 이것이 진짜 비선형 층.

## 재현
```bash
./run.sh   # (참고: run.sh은 기본 실험; MVP는 아래)
source .venv/bin/activate && source .env
python -m runner.run_mvp          # 96 호출 → data/mvp_runs.jsonl
python -m analyze.analyze_mvp     # → data/mvp_analysis.json
```
설정: `runner/mvp_config.json`(모델·목적·바인딩·반복).