# Routing Matrix — Data-Grounded Purpose-to-Model Routing (Draft)

> 한국어 버전: [`ROUTING.ko.md`](ROUTING.ko.md) · Experiments index: [`../EXPERIMENTS.en.md`](../EXPERIMENTS.en.md)

A **purpose-to-model routing proposal** distilled from the raw JSON of all three
experiments (Exp1 120 / Exp2 96 / Exp3 75 runs). An earlier Pruner v1 proposal — a
"hybrid matrix (synthesize→local, decide→cloud reasoning)" — conflicted with the data; this
document replaces it with a **purpose-bifurcated, data-consistent** version.

## 0. Why this replaces the v1 matrix

The earlier Pruner matrix contradicts the data in two ways.

1. **decide → cloud reasoning**: per Exp2 `decide_stance_by_model`, the reasoning family
   (deepseek = qualified 2, gpt-oss = yes 1 + qualified 1) emits *hedging, not a decisive
   verdict*. Routing decide to reasoning therefore yields a conditional hedge, not the
   "decision" the purpose asks for — the matrix's intent and the model's output diverge.
2. **synthesize → local 1B wholesale**: on the Exp2 `synth_novelty` (**cross-model**) metric,
   `gemma4:31b` = 0.764 is **last of 8 models**. "Local 1B's novelty 0.995" is Exp3's
   `within_item_novelty` (**repetition dispersion**) — a *different* measure from Exp2's
   novelty (distinctiveness vs other models; see the caveat footnote), so "local dominates
   originality" does not hold.

→ Hence **decide** and **synthesize** are each **bifurcated into sub-purposes**, and routing
is defined to be data-consistent.

## 1. Data-grounded routing matrix

| Purpose $P$ (bifurcated) | Optimal $M^*$ | Evidence (raw JSON) | Cost | Marker |
|---|---|---|---|---|
| **decide · decisive verdict** (binary commit required) | `gemma4:31b` (small-efficient) | Exp2: `minimum_wage` **yes 2/2 alone**; reasoning models hedge | paid (low) | 1.0 |
| **decide · cautious hedge / multi-factor review** | reasoning family (`gpt-oss:120b`, `deepseek-v4-flash`) | Exp2: qualified (risk-averse); `has_verdict_marker`=1.0 | paid (high) | 1.0 |
| **synthesize · repetition-dispersion divergence** (brainstorm) | local `gemma3:1b` | Exp3: `within_item_novelty`=**0.995**; `mean_marker_rate`=1.0 | **free** | 1.0 |
| **synthesize · cross-model originality** | `gpt-oss:120b` | Exp2: `synth_novelty`=**0.894** (top of 8); `has_synthesis_marker`=1.0 | paid (high) | 1.0 |
| **surface_assumptions** (data thin) | lowest-cost model (type-independent) | Exp2: `realization_by_model_type` all types `surface_assumptions`=**1.0** | min | 1.0 |
| **(exclude) when marker stability is critical** | gemma family + reasoning; **exclude kimi-k2.6, llama3.2:\*** | Exp2: kimi `decide` marker **0.5**; Exp3: llama 1b/3b marker 0.933/0.8 | — | risk |

## 2. What changed vs the v1 matrix

| Item | v1 proposal | Data-grounded correction | Basis |
|---|---|---|---|
| decide routing | "cloud reasoning" (single) | **decisive→gemma4:31b / hedge→reasoning** bifurcation | reasoning hedges (②); only gemma is decisive yes |
| synthesize routing | "local 1B~4B" wholesale | **dispersion→local 1B / originality→gpt-oss** bifurcation | the two novelties differ (D); on cross-model gemma is last |
| Llama family | unspecified | **exclude for all purposes** (marker 0.8–0.933, meta-utterance) | Exp3 llama scale-reversal + syntax leakage |
| kimi-k2.6 | implicit "cloud MoE" | **exclude for decide/synthesize** (marker 0.5) | Exp2 kimi decide marker 0.5 (verbosity 10,016 chars) |

## 3. Routing pseudocode (linear wiring)

```
route(P):
  if P == decide:
      sub = J(P)              # human gate: which sub-purpose — "decisive verdict" or "cautious hedge"?
      if sub == "decisive":   return M* = gemma4:31b
      if sub == "cautious":    return M* = gpt-oss:120b | deepseek-v4-flash
  if P == synthesize:
      sub = J(P)              # human gate: "repetition dispersion" or "cross-model originality"?
      if sub == "dispersion": return M* = gemma3:1b (local, free)
      if sub == "originality":return M* = gpt-oss:120b
  if P == surface_assumptions: return M* = min_cost_model()   # type-independent marker 1.0
  # guardrail: allow gemma family + reasoning only; exclude kimi, llama
```

The human $J$ gate is used **only to pick the sub-purpose** of decide/synthesize (not
automatable — this is exactly why $\Phi$ stays a black box). Once $J$ picks the sub-purpose,
the routing is deterministic (linear).

## 4. The non-linear black box (deferred)

`[Prerequisite Black Box Φ]` — the function that, given purpose $P$, jointly fixes the ideal
template *and* model in one shot. Exp1 (verdict variance 0.283), Exp2 (same form → model-split
verdicts), and Exp3 (novelty↔concreteness anti-correlation) all show that a single binding
cannot guarantee a correct outcome. This matrix is an **outer approximation** of $\Phi$:
$J$ picks the sub-purpose, then linear routing takes over. $\Phi$'s interior (auto
sub-purpose detection, promoting 1B's rhetorical cheat to genuine creativity, distilling 12B
concreteness at low cost) is unresolved and deferred as the lower-layer ideal $I_1$.

## 5. Caveats
- **Stance-heuristic dependence**: the "decisive verdict" basis (gemma yes 2/2) is the output
  of `analyze_mvp.py`'s keyword-stance heuristic; no qualitative-$J$ cross-check yet.
- **Small n**: decide 2 repeats × 2 items; synthesize 2/5 items. Routing confidence is low.
- **cross/within novelty not comparable**: see §0.2 and the caveat footnote. Mixing the two
  produces the "local 1B dominates" misreading.
- **Local 1B concreteness**: Exp3 shows gemma3:1b's syntheses trend toward abstract
  rhetorical gaslighting (third_word_count 0.73 but low operational concreteness). The
  "repetition-dispersion divergence" route buys *breadth of dispersion*, not *concrete
  design* — concrete design is the 12B / gpt-oss domain.

## Reproduction / sources
- Data: `data/mvp_analysis.json` (Exp2), `data/exp3_analysis.json` (Exp3), `data/analysis.json` (Exp1)
- Metric definitions: `analyze/analyze_mvp.py`, `analyze/analyze_exp3.py`
- This matrix is an **outer approximation** of the experimental data; opening $\Phi$'s
  interior is a follow-up task.