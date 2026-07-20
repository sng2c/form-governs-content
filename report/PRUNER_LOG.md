# Pruner 세션 로그 — form-governs-content 가지치기 기록

> **v0.3.0 정합 뷰는 [`CONTROL_PANEL.md`](CONTROL_PANEL.md) / [`CONTROL_PANEL.en.md`](CONTROL_PANEL.en.md) 로 이전**. 본 파일은 *과거 세션 기록(역사적)*로 보존. 용어(Φ·블랙박스·하강)는 v0.2 시점것이며, v0.3.0(정합적 이상·제어판·환상 컨트롤 삭제)로 재정렬한 결과는 CONTROL_PANEL에 있음.
> 라우팅 산출물은 [`ROUTING.ko.md`](ROUTING.ko.md) · [`ROUTING.md`](ROUTING.md) 참고.
> **PC 재개 시 이 파일을 먼저 읽으면 세션 맥락이 복원된다.**

---

## 세션 개요
- **대상 데이터**: Exp1(120회, 단일모델 8형식) · Exp2(96회, 클라우드 8모델) · Exp3(75회, 로컬 소형 5모델) — raw JSON은 `data/{analysis,mvp_analysis,exp3_analysis}.json`
- **목표**: "형식이 내용을 지배한다" 데이터에서 비용 0원 로컬 창의적 종합 파이프라인 아키텍처 가지치기
- **스킬**: pruner-arch (4-단계 백캐스팅, 비선형 노드를 블랙박스로 연기, 인가 게이트 대기)

## Layer 1 — 목적별 라우팅 매트릭스 (머지됨 → `report/ROUTING.*`)
- **$I_0$**: 형식 $F$ 투입 시 4불변량 $\mu$(마커)=1.0 · $\rho$(이항거부)=1.0 · $\nu$(novelty)=max · $\kappa$(concreteness)=max 동시 만족
- **비선형 병목**: $\nu \leftrightarrow \kappa$ 역상관 (novelty 수치상 1B > 12B but 구체성 역전)
- **블랙박스 I_3**: Novelty-Concreteness Allocator $\Phi$ — 자동 라우팅 내부 연기
- **MVP**: 목적 $P$ → 결정론적 라우팅($\Phi$ 외부 근사) → `report/ROUTING.*`로 산출
- **정정**: 기존 "하이브리드 매트릭스(synthesize→로컬, decide→reasoning)"는 ②(reasoning=qualified 회피)·③(novelty 메트릭 불일치)와 자기모순 → decide·synthesize 각각 이항 분해로 정합화

## Layer 2 — 종합 진정성 자동 판별 (대화 설계, 미산출)
- **$I_0^{(2)}$**: $\Phi$가 인간 $J$ 없이 자동으로 $(M^*,\theta^*)$ 배정 + $S_3$ 진정성 보증
- **비선형 병목 $B_2$**: 1B 종합 "진정성" 자동 판별 — $\nu$ 로 품질 불가 (1B 수사 치트 오인 위험)
- **블랙박스 I_4**: Synthesis Authenticity Judge $J_{\text{auto}}(S_3,C)\to$ authenticity
- **MVP**: concreteness 가드레일 — 1B 출력 중 operational 구조 부족 시 12B 승격

## Layer 3 — 지양(Sublation) 자동 판별 (대화 설계, 미산출)
- **$I_0^{(3)}$**: $J_{\text{auto}}$가 $S_3 \triangleright (A \wedge B)$ (정·반을 지양하는 상위 범주) 자동 판별
- **정정 발견**: 고유명사 *유무*로는 1B·12B concreteness 구분 불가(둘 다 명명) → 진짜 차별은 **operational 작동 구조 묘사**. Layer 2 `concreteness_proxy`를 "고유명사 밀도"→"operational 동사·작동구조 밀도"로 정제
- **비선형 병목 $B_3$**: sublation 관계 자동 측정 — embedding에 "지양" 축 없음
- **블랙박스 I_5**: Sublation Detector $\Sigma(S_3,A,B)\to$ sublation
- **MVP**: embedding "단순 보간 아님" + 정제 operational_proxy **2중 선형 가드레일** ($\Sigma$ 외부 근사)
- **🚨 선형화 장애물**: 임계값 $\theta$ 캘리브레이션에 **라벨링 교정 셋 필요** but `data/*_runs.jsonl`이 **git 제외** → 원시 response 부재. **raw 보존이 모든 추가 선형화의 선행 조건**

## 핵심 정정 기록 (세션 중 발견)
1. **stance 정정** (PR #1): MVP §2 verdict 표가 `mvp_analysis.json`과 불일치 → 데이터 기준 재작성 (gemma4:31b=단호 yes 2/2 단독)
2. **novelty 메트릭 불일치** (PR #1): Exp2 cross-model vs Exp3 within-item은 다른 측정량 → 직접 비교 무효 경고
3. **매트릭스 자기모순** (PR #2): decide→reasoning 은 ②와 충돌 → decide·synthesize 이항 분해
4. **12B 비용 0 정정** (PR #2): `gemma4:12b-mlx`는 로컬 MLX → 독창성 라우팅을 gpt-oss(유료)에서 로컬 12B(0원)로 전환, 가드레일 비용 분기 제거

## 머지 이력 (main 반영 완료)
- PR #1 `fix/mvp-stance-and-novelty-metric` — 머지됨 (`e4f419e`)
- PR #2 `feat/routing-matrix-data-grounded` — 머지됨 (`457fdca`, 12B 정정 포함 2커밋 squash)
- 작업 브랜치 정리 완료, 현재 `main` 단독

---

## 🟡 현재 대기 지점 — Layer 3 `[I_5: Σ]` Awaiting
PC 재개 시 아래 4옵션 중 하나 선택:

1. **Layer 3 승인** — 2중 선형 가드레일(embedding + operational_proxy) MVP 동결
2. **Σ 하강** — Layer 4 재귀 가지치기 (지양 관계 자동 측정법)
3. **raw 보존 우선** ⭐ 제안 — `runner/run_*.py`에 raw response 전체 저장 추가 → `data/*_runs.jsonl` 커밋 → 임계값 θ 캘리브레이션 교정 셋 확보. **현재 유일한 선형화 장애물**.
4. **로컬 12B 보완 실험** — 로컬 `gemma4:12b-mlx`로 (a) `red_blue_debate`(decide) 폼, (b) cross-model novelty 측정 실행 → ROUTING 매트릭스의 미측정 라우팅(decide·독창성) 보완

### PC 재개 권장 순서
**옵션 3 → 4 → (1 or 2)**. raw 보존이 임계값 산출의 선행 조건이고, 12B 보완 실험이 그 위에 올 미측정 라우팅을 채운다. 그 후 Layer 3 승인 또는 Σ 하강 선택.

### 재개 트리거
"PRUNER_LOG 읽었어, 3번" 또는 "3+4 같이" 정도로 말하면 바로 이어감.