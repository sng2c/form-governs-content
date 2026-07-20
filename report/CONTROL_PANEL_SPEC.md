# 제어판 설계 — `pruner-dialectic` (v0.3.0 발견 메커니즘의 명문화)

> 영문: [`CONTROL_PANEL_SPEC.en.md`](CONTROL_PANEL_SPEC.en.md) · 정합 뷰: [`CONTROL_PANEL.md`](CONTROL_PANEL.md)
> 이 문서는 Pruner v0.3.0 하강이 *발견*(설계 아님)한 제어판의 인터페이스를 명문화한 것이다. $I_0$(완전 자동)은 환상으로 확정됐고, 살아남은 두 컨트롤(`intent`, $\alpha$)이 소멸 저항(실재)했으므로, 이제 그 인터페이스를 구체화한다.

## 0. 계약 (Contract)
> **완전 자동, 단 두 개의 외과적 인간 게이트 — 각각 자기 트리거가 발동할 때만 노출.** 전자동이 목표가 아니라 *최소·외과적 인간 통제*가 목표. 대다수 실행은 0개의 컨트롤을 노출한다.

## 1. 자동 코어 (노출 컨트롤 없음)
```
(P, C) → [형식 바인딩] → [모델 라우팅] → [실행 M(F,C)] → S3 → [프록시 산출 m,ρ,ν,κ_op]
```
- **형식 바인딩**(고정, Exp1/2): `decide→red_blue_debate` · `synthesize→dialectical_triad` · `surface_assumptions→socratic_dialogue`
- **모델 라우팅**(매트릭스, Exp2/3): `synthesize/surface→최저 로컬(gemma3:1b/4b)` · `decide-명확→저가` · `decide-쟁점→reasoning(gpt-oss)`(단 `intent` 아래 변동)
- **프록시**: $m, \rho, \nu, \kappa_{\text{op}}$ 자동 산출. *좁히기 전용* — Stage B가 G/C 분리 불가를 보였으므로 프록시는 판정하지 않는다.

## 2. 컨트롤 #1 — `intent` (편향 방향 스위치)
| 항목 | 값 |
|---|---|
| 트리거 | $P=\text{decide}$ AND 쟁점 수위 $r(C)\ge\theta_r$ |
| 인간 입력 | `{scrutinize(보수 검증·lean no) \| include(점진 포용·lean yes) \| neutral}` |
| 효과 | 선택 편향에 맞는 모델/스탠스로 라우팅 |
| 비노출 | decide가 아니거나 $r<\theta_r$ → 자동 `neutral` |
| 왜 인간 | 정답 없는 가치 판단(Exp2: 모델별 support/opose 관측) |

## 3. 컨트롤 #2 — $\alpha$ (진정성 게이트)
| 항목 | 값 |
|---|---|
| 트리거 | $S_3$가 경계 영역 — 프록시 flag: $\nu\ge0.999$ AND $\kappa_{\text{op}}\le3.7$ (Stage A candidate-cheat 영역) |
| 인간 입력 | $S_3$ + 관측량 + 비교 표시 → `G(진짜 지양) \| C(cheat) \| B(경계)` |
| 효과 | G→수용 · C→강한 모델로 재라우팅/재실행 · B→인간 결정 |
| 비노출 | 명확 사례(프록시 일치/미flag) → 자동 수용 |
| 왜 인간 | 관측량이 G/C 분리 불가(Stage B: 18쌍 관측 동일, 로지스틱 0.625) — 불가결 판단 |

## 4. 임계값 (데이터 기반 시드)
- **$\theta_r \approx 0.30$** — Exp1 verdict 분산 기준: `battery 0.20 · pluto 0.225 < 0.30 < minimum_wage 0.425`. → min_wage만 `intent` 발동, battery/pluto는 자동.
- **$\alpha$ 경계 영역** — Stage A: $\nu\ge0.999$ AND $\kappa_{\text{op}}\le3.7$.
- 두 임계값 모두 *시드*; raw 보존(옵션3 완료) 위에서 교정 가능.

## 5. 최소화 (패널이 줄어드는 모습)
| 실행 유형 | 노출 컨트롤 |
|---|---|
| synthesize / surface (대다수) | **0** |
| decide-명확 | 0 |
| decide-쟁점 (예: min_wage) | **intent** |
| 임의 P, $S_3$ 경계 flag | **$\alpha$** |
| decide-쟁점 + $S_3$ 경계 (드묾) | **intent + $\alpha$** |

## 6. 증거 기반 (각 요소를 확정한 실험)
- 형식=내용 지배 → **Exp1**(verdict 분산 0.283).
- 모델 라우팅 대부분 소멸(synthesize/surface 모델 무관) → **Exp2/3**(1B robust).
- `intent` 실재(decide-쟁점 판정 모델 의존) → **Exp2**(min_wage support/oppose 분기).
- $\alpha$ 후보 부상(1B novelty-cheat 위험) → **Exp3**.
- $\alpha$ 실재(관측량으로 소멸 불가) → **Stage B**(본 라벨링).
- $I_0$(완전 자동) 환상 확정 → **Stage B**($\alpha$ 소멸 불가 $\Rightarrow$ 완전 자동 불가).

## 7. 상태
- v0.3.0 **종료 조건 도달**: 두 컨트롤 모두 소멸 저항(실재), 더 삭제할 환상 컨트롤 없음.
- 본 설계는 *발견된* 제어판의 인터페이스 명문화. 구현(자동 코어 + 두 게이트 노출 로직)은 다음 단계.

## 8. 미구현(명문화 한계)
- 자동 코어의 라우팅 매트릭스·프록시 산출은 코드로 구현되어 있으나(`runner/`·`analyze/`), *게이트 노출 로직(intent/α 트리거 시 인간에게 보여주고 입력 받는 흐름)* 은 아직 구현 안 됨. 이 설계가 그 구현의 계약(spec) 역할.