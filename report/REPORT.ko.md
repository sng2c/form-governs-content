# 형식이 내용을 지배한다 — LLM 안에서의 경험적 검증 (상세 리포트)

> 영문 버전: [`REPORT.md`](REPORT.md) · 항목별 상세: [`ITEMS.ko.md`](ITEMS.ko.md)
> **v0.3.0 독해**: 이 실험은 제어판 후보 $\Phi_0$(이상 템플릿 생성)의 숨은 가정("템플릿이 내용과 무관")을 *정정*하고, 창의성=형식 주도의 첫 증거를 제공. 정합 뷰: [`CONTROL_PANEL.md`](CONTROL_PANEL.md).

## 헤겔의 명제
헤겔의 《논리학》에서 형식은 내용을 담는 무관한 그릇이 아니다. 형식은 내용의
*규정성*이다 — "형식은 규정된 내용 그 자체"이다. 따라서 형식을 바꾸는 것은
표시 방식을 바꾸는 게 아니라 *내용이 무엇인지*를 바꾸는 것이다. "Die Form
regiert den Inhalt": 형식이 내용을 지배한다.

## 작동적 질문
이것이 LLM 안에서도 성립한다면, 모델에게 **같은 사실과 같은 질문**을 주되
**다른 형식**을 입혔을 때 산출물이 단지 화법만 바뀌는 게 아니라 *실질적 내용*
(판정·추론 경로·진리 판정)이 달라져야 한다.

## 무엇을 했는가 (설계)
- 3개 통제 항목(중립 사실 + 진짜 쟁점 질문): `battery_limits`, `minimum_wage`,
  `pluto_planet`. *각 항목의 질문·사실·설계 의도·형식별 결론은 [`ITEMS.ko.md`](ITEMS.ko.md)에 상세.*
- 8개 형식, 2개 계열:
  - *재배열형*(불릿·단계·JSON·Q&A·삼단논법): 내용을 재배열.
  - *생성형*(변증법 triad·소크라테스 대화·찬반 토론): 내용을 모순을 통해 발전.
- 각 (콘텐츠 × 형식) 셀을 **5회** 반복, 시드 변화(42–46), 고정 모델
  (`gpt-oss:120b`, Ollama Cloud), 온도 0.3, max_tokens 4096 → **120 completions**.
- 각 산출물에서 결론 문장 추출 후 스타일 제거(단일 문장으로 정규화).
- 두 가지 측정:
  - **TF-IDF 표면 비율** = 형식 간 코사인 거리 ÷ 형식 내 코사인 거리.
  - **verdict 분산(스타일 제거)**: 결론을 항목별 stance 라벨로 분류; 분산 =
    `1 − (최대 라벨 점유율)`. 높으면 같은 내용에서 형식이 *판정*을 좌우 → 형식이
    내용 지배.

## 결과

### 핵심 수치 (`data/analysis.json`)
| 측정 | 값 | 해석 |
|---|---|---|
| TF-IDF 표면 비율 (across/within) | **1.19** | >1 (형식 효과)이지만 엄격 기준 1.5 미만. 표면 노이즈에 의해 과소평가. |
| within-form 분산 (재배열 / 생성) | 0.73 / 0.85 | 생성형이 반복에서도 표면이 더 다양 — "발전"하는 형식의 특성. |
| **verdict 분산(스타일 제거), 전체** | **0.283** | 같은 내용에서 형식만 바꿨을 때 판정이 갈리는 비율. |
| `hegel_h1_verdict` (분산 > 0.15) | **true** | **내용(판정) 수준에서 H1 성립.** |
| `hegel_h1` (TF-IDF 비율 > 1.5) | false | 표면 측정은 스타일 누출로 과소탐지. |

### Verdict × 형식 (깨끗한 신호)
같은 내용, 다른 형식 → 다른 판정:

**minimum_wage** — *가장 강력한 형식-지배-내용 효과 (분산 0.425)*
분포: qualified 23, support 14, oppose 3.
| 형식 | 판정 |
|---|---|
| bullet_list | qualified (5/5) |
| numbered_steps | qualified (4) / support (1) |
| **json_schema** | **oppose 2 / support 1 / qualified 2 — 부정으로 기운 유일한 형식** |
| qa_pairs | qualified (3) / support / oppose |
| syllogism | qualified (4) / support (1) |
| **dialectical_triad** | **qualified (5/5) — 이항을 거부하고 종합을 생산** |
| **socratic_dialogue** | **support (5/5)** |
| **red_blue_debate** | **support (5/5)** |

→ 두 *대화/대립형* 생성 폼은 깔끔하게 **"지지"**에 커밋, 구조적 분석 폼은
**"qualified"**로 헤징, 경직된 **JSON** 폼만 **"oppose"**로 기움. 같은 사실,
다른 형식, 다른 판정.

**pluto_planet** — 분산 0.225. 대부분 **"재분류(reclassify)"**로 수렴;
**`red_blue_debate`**만 **"왜소행성 유지"**로 기움(대립/판사 형식이 공식 개정
대기의 보수적 판정을 내놓는 경향); `bullet_list`도 "왜소행성 유지"로 기움
(목록 형식이 IAU 기준을 장애물 목록으로 표면화).

**battery_limits** — 분산 0.20. 사실이 한쪽을 강하게 지지해 대부분
**"조건 없이(no contingency)"**로 수렴; 약한 분기(syllogism / json_schema /
red_blue가 5회 중 2회 "pro_contingency").

### 계열별 (재배열 vs 생성)
- 생성형이 **within-form 표면 분산이 더 큼**(0.85 vs 0.73): 같은 형식 반복에서도
  더 다양한 텍스트 — *발전*하는 형식의 특성.
- 생성형이 **더 단호한 판정**을 내림: minimum_wage에서 socratic_dialogue와
  red_blue_debate가 5/5 "support"인 반면 재배열 폼은 헤징.

### 헤겔 변증법 triad (H1a)
`dialectical_triad`는 minimum_wage에서 **"qualified" 5/5**를 반환한 유일한 형식은
아니지만, 가장 일관되게 *이항을 거부*하고 인플레이션 연동·지역 조정·안전장치의
*제3의 종합적 판정*을 만들어낸다. 이것이 헤겔 예측: triad는 극 중 하나를 고르지
않고 양극의 내용을 보존·지양(Aufhebung)하는 *새로운 차원의 결정*을 생산. 형식이
내용을 재배열한 게 아니라 **다른 종류의 내용을 생산**.

## 해석: LLM에서 형식은 내용을 지배하는가? — **내용 수준에서 그렇다.**
- 표면(TF-IDF) 측정은 약한 신호(비율 1.19)만 준다. reasoning 모델은 같은 형식을
  반복해도 표면 실현이 노이즈하기 때문에 within-form 분모가 부풀려진다.
- **스타일 제거 verdict 측정**은 같은 중립 사실·같은 질문에서 모델의 *대답*이
  형식에 따라 ~28% 바뀌고, 가장 쟁점적인 항목(minimum_wage)에서는 ~43% 바뀜을
  보여준다.
- 형식의 *유형*이 헤겔 식으로 중요: 변증법 triad는 체계적으로 제3의 종합적 판정을
  만들고; 대립 형식은 보수적 판정이 기본이며; 경직된 JSON 형식만 부정으로 넛징.
  각 형식은 특성적 *스타일*이 아니라 특성적 *내용*을 가진다.

**결론:** 내용을 고정한 채 "단지" 형식을 바꿀 수는 없다. 형식은 이미 결과의
규정의 일부다. 헤겔의 명제가 LLM 안에서 — 스타일 효과가 아니라 실질적 효과로 —
재현되었다.

## 한계 / 다음 단계
- **n=3항목 × 5반복**은 파일럿. 검정력을 위해 항목·반복 확대 필요.
- verdict 분류는 항목별 키워드 휴리스틱. **LLM-judge** 추출 단계가 휴리스틱을
  제거하고 임의 항목을 가능하게 함.
- TF-IDF는 스타일 누출; sentence-embedding이나 LLM-judge로 교체하면 내용/스타일
  분리가 더 타이트해짐.
- `seed` 재현성은 유지됐으나 reasoning 모델의 표면 비결정성은 실재; verdict 측정이
  설계상 이에 robust.
- minimum_wage 결과가 가장 강력한 단일 증거이므로, 증거가 진짜 균형 잡힌 항목을
  더 늘려 전용 복제가 필요.

## 재현
```
./run.sh experiments   # 120 호출 → data/raw_runs.jsonl
./run.sh analyze       # → data/analysis.json
```
설정은 `runner/config.json`; 비밀키·venv 경로는 `.env`.