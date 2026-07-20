# 라우팅 매트릭스 — 데이터 정합 목적별 모델 라우팅 (초안)

> 영문 버전: [`ROUTING.md`](ROUTING.md) · 실험 인덱스: [`../EXPERIMENTS.md`](../EXPERIMENTS.md)
> **v0.3.0 독해**: 이 매트릭스는 자동 코어의 구현 + `intent` 컨트롤의 구체화. $\Phi_{\text{route}}$의 *소멸된 부분*(자동 라우팅)과 *저항한 잔여*(`intent` 스위치)가 함께 살아 있음. 정합 뷰: [`CONTROL_PANEL.md`](CONTROL_PANEL.md).

세 실험(Exp1 120회 / Exp2 96회 / Exp3 75회)의 raw JSON에서 도출한 **목적별 모델 라우팅 제안**이다.
이전 Pruner 1차 제안의 "하이브리드 매트릭스(synthesize→로컬, decide→클라우드 reasoning)"는
데이터와 내적 충돌하여, 이 문서에서 **목적을 이항 분해하여 정합시킨 정본**으로 대체한다.

## 0. 정정 배경 — 이전 제안의 자기모순

이전 Pruner 매트릭스는 두 가지로 데이터와 충돌한다.

1. **decide → 클라우드 reasoning**: Exp2 `decide_stance_by_model`에 따르면 reasoning
   계열(deepseek=qualified 2, gpt-oss=yes 1+qualified 1)은 *확정 판정이 아니라 유보*를 낸다.
   즉 "decide(판정)에 reasoning을 배정하면 확정 판정이 아니라 조건부 유보가 나온다" —
   매트릭스의 목적(판정)과 결과(유보)가 어긋난다.
2. **synthesize → 로컬 1B 일괄**: Exp2 `synth_novelty`(cross-model) 기준으로는
   `gemma4:31b`=0.764로 **8종 최하위**다. "로컬 1B의 novelty 0.995"는 Exp3의
   `within_item_novelty`(**반복 분산**)로, Exp2의 novelty(**타 모델 대비 독창성**)와는
   다른 측정량이므로(각주 경고 참조) "로컬 1B가 독창성 압도"는 성립하지 않는다.
   **단, 로컬 12B `gemma4:12b-mlx`는 클라우드 비용 없이(로컬 MLX) gpt-oss:120b와
   정성 동등한 종합을 산출(Exp3 동기 관찰)하므로, "독창성" 라우팅의 1순위는 로컬 12B다** —
   gpt-oss는 cross novelty 수치 비교 기준으로만 표기(로컬 12B의 cross novelty는 미측정).

→ 따라서 **decide**와 **synthesize** 각각을 **하위 목적으로 이항 분해**하여, 데이터와
정합하는 라우팅을 정의한다.

## 1. 데이터 정합 라우팅 매트릭스

| 목적 $P$ (이항 분해) | 최적 $M^*$ | 근거 (raw JSON) | 비용 | 마커 안정 |
|---|---|---|---|---|
| **decide · 확정 판정** (이항 커밋 요구) | `gemma4:31b` (클라우드 small-efficient) | Exp2: `minimum_wage` **yes 2/2 단독**; reasoning 모델은 qualified 회피 | 유료(저) | 1.0 |
| **decide · 신중 유보 / 다변수 검토** | reasoning 계열 — `gpt-oss:120b`/`deepseek` (클라우드) **또는 로컬 `gemma4:12b-mlx`(후보)** | Exp2: 클라우드 reasoning은 qualified로 위험 회피; 로컬 12B는 reasoning이나 `red_blue_debate` 폼 **미측정** | 유료 **또는 0원** | 1.0 |
| **synthesize · 반복 분산 발산** (브레인스토밍) | 로컬 `gemma3:1b` | Exp3: `within_item_novelty`=**0.995**; `mean_marker_rate`=1.0 | **0원** | 1.0 |
| **synthesize · 독창성** (명명·정성 동등) | **로컬 `gemma4:12b-mlx`** (1순위) / `gpt-oss:120b` (비교 기준) | Exp3: 로컬 12B가 gpt-oss와 정성 동등 + "Aggregated Urbanism" 등 명명 + marker 1.0; Exp2: `gpt-oss` `synth_novelty`=0.894(cross 측정값, **로컬 12B는 미측정**) | **0원** | 1.0 |
| **surface_assumptions** (데이터 부족) | 로컬 최소비용 모델 (타입 무관) | Exp2: `realization_by_model_type` 전 타입 `surface_assumptions`=**1.0** | **0원** | 1.0 |
| **(배제) 마커 안정성 중시 시** | gemma 계열 + reasoning; **kimi-k2.6·llama3.2:* 배제** | Exp2: kimi `decide` marker **0.5**; Exp3: llama 1b/3b marker 0.933/0.8 | — | 위험 |

## 2. 정정 포인트 — 이전 매트릭스와의 차이

| 항목 | 이전 제안 | 데이터 정합 정정 | 근거 |
|---|---|---|---|
| decide 라우팅 | "클라우드 reasoning" 단일 | **확정판정→gemma4:31b / 유보→reasoning** 이항 분해 | reasoning은 qualified 회피(②), gemma만 단호 yes |
| synthesize 라우팅 | "로컬 1B~4B" 일괄 | **반복분산→로컬 1B / 독창성→로컬 12B**(gpt-oss는 비교기준)** 이항 분해 | 두 novelty 정의 상이(D); **로컬 12B 비용 0 + 정성 동등** |
| Llama 계열 | 명시 없음 | **전 목적 배제** (마커 0.8–0.933, 메타 발화) | Exp3 llama 스케일 역전·구문 누출 |
| kimi-k2.6 | "클라우드 MoE" 묵시 | **decide/synthesize 배제** (marker 0.5) | Exp2 kimi decide marker 0.5 (과잉 장황 10,016자) |

## 3. 라우팅 의사결정 의사코드 (선형 결선)

```
route(P):
  if P == decide:
      sub = J(P)              # 인간 게이트: "확정 판정" vs "신중 유보" 중 무엇을 원하는가?
      if sub == "확정 판정":   return M* = gemma4:31b
      if sub == "신중 유보":   return M* = gpt-oss:120b | deepseek-v4-flash
  if P == synthesize:
      sub = J(P)              # 인간 게이트: "발산(반복 분산)" vs "독창성(타 모델 대비)" ?
      if sub == "반복 분산":   return M* = gemma3:1b (로컬, 0원)
      if sub == "독창성":      return M* = gpt-oss:120b
  if P == surface_assumptions: return M* = min_cost_model()   # 타입 무관 marker 1.0
  # 가드레일: gemma 계열 + reasoning만 허용; kimi·llama 배제
```

인간 $J$ 게이트는 decide·synthesize 각각의 **하위 목적 판별**에만 쓰인다(자동화 불가 — 이것이
$\Phi$가 블랙박스로 남은 이유). $J$가 하위 목적을 결정하면 그 뒤 라우팅은 결정론적(선형)이다.

## 4. 비선형 블랙박스 (연기)

`[Prerequisite Black Box Φ]` — 목적 $P$를 주면 이상 템플릿+모델을 한 번에 정하는 함수.
Exp1(verdict 분산 0.283)·Exp2(같은 형식인데 모델별 판정 분기)·Exp3(novelty↔구체성 역상관)
모두 "단일 바인딩으로는 올바른 결과 보장 불가"를 입증. 본 매트릭스는 $\Phi$의 **외부 근사**로,
$J$가 하위 목적을 고르면 선형 라우팅이 작동하도록 설계한 것. $\Phi$ 내부(하위 목적 자동 판별,
1B 수사 치트의 진정 창의성 승격, 12B 구체성의 저비용 증류)는 미해결이므로 **하위 레이어의
이상 $I_1$**으로 연기한다.

## 5. 한계
- **stance 휴리스틱 의존**: decide 라우팅의 "확정 판정" 근거(gemma yes 2/2)는
  `analyze_mvp.py`의 키워드 stance 휴리스틱 결과. 정성 $J$ 교차검증 미수행.
- **n 작음**: decide 2반복·항목 2개, synthesize는 항목 2/5개. 라우팅 확정도 낮음.
- **cross/within novelty 비교 불가**: §0.2·각주 경고 참조. 두 novelty를 혼용하면
  "로컬 1B 우위"라는 오독 발생.
- **12B 비용 정정**: 로컬 `gemma4:12b-mlx`는 MLX 가속 로컬 모델로 **비용 0원**.
  따라서 "독창성" 라우팅과 가드레일 승격(1B→12B) 모두 비용 분기 없이 0원.
  gpt-oss:120b는 cross novelty 수치가 측정된 비교 기준일 뿐, 비용에서 로컬 12B가 우위.
- **로컬 12B 독창성 미측정**: 로컬 12B의 cross-model novelty는 Exp3에 메트릭이 없어
  미측정. "독창성 1순위 로컬 12B"는 정성 동등 + 비용 0 근거지, cross 수치 근거 아님.
- **decide 로컬화 미측정**: 로컬 12B는 reasoning이나 `red_blue_debate`(decide) 폼
  미실행. decide "신중유보" 로컬 12B 후보는 미검증.
- **로컬 1B의 구체성**: Exp3에서 gemma3:1b의 종합은 추상 가스라이팅(수사 치트) 경향
  (third_word_count 0.73이지만 운용 구체성 낮음). "반복 분산 발산" 라우팅은 *발산의
  폭*이지 *구체 설계*가 아님 — 구체 설계는 **로컬 12B** 영역.

## 재현 / 출처
- 데이터: `data/mvp_analysis.json` (Exp2), `data/exp3_analysis.json` (Exp3), `data/analysis.json` (Exp1)
- 메트릭 정의: `analyze/analyze_mvp.py`, `analyze/analyze_exp3.py`
- 본 매트릭스는 실험 데이터의 **외부 근사**이며, $\Phi$ 내부를 여는 것은 후속 과제.