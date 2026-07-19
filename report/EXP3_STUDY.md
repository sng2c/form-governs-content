# Exp 3 — Dialectical Triad Aufhebung Verified on a Small Local Model

> 한국어 버전: [`EXP3_STUDY.ko.md`](EXP3_STUDY.ko.md) · Experiments index: [`../EXPERIMENTS.en.md`](../EXPERIMENTS.en.md)

## Motivation
Exp 2 showed cloud `gemma4:31b` producing a qualitatively equivalent synthesis to
gpt-oss:120b under the triad (novelty 0.764). This raised the hypothesis (H_local):
**if the triad form's synthesis power is robust to model scale/type, creative
problem-solving is feasible on a small local LLM — without expensive cloud reasoning
models.** This experiment verifies H_local directly on a local model.

## Hypothesis (H_local)
> The dialectical triad's Aufhebung (refuse the binary → produce a third synthesis) is
> robust to model scale/type, so **a small local model (12B MLX) can perform creative
> problem-solving (produce a third design proposition) under the triad form.**

## Design
- **Fixed form**: `dialectical_triad` only (the source of creativity = the form).
- **Local model**: `gemma4:12b-mlx` (7.7GB, MLX-accelerated, reasoning model) via local
  Ollama (`localhost:11434`).
- **5 content items**: 3 existing contested items + **2 open-ended design items**
  (`freshwater_alloc`, `density_greenspace` — no single correct answer, forcing a genuine
  third design rather than picking a side).
- **3 repeats**, same seed/temperature/max_tokens. **15 local calls** (free, ~6 min/item).
- **Measures**: `SYNTHESIS CONCLUSION` marker, refuses-binary, third-proposition keywords,
  within-item novelty (creative variance). **Key = human $J$**: qualitative judgment that
  each synthesis is a genuine third proposition, not a simple sum of the poles.

## Results (`data/exp3_analysis.json`)

### Quantitative — Aufhebung reproduced 100% on local 12B
| item | marker | refuses_binary | third-words | novelty |
|---|---|---|---|---|
| battery_limits (contested) | 1.0 | 1.0 | 0.33 | 1.0 |
| minimum_wage (contested) | 1.0 | 1.0 | 0.0 | 0.94 |
| pluto_planet (contested) | 1.0 | 1.0 | 0.67 | 1.0 |
| freshwater_alloc (**open**) | 1.0 | 1.0 | 0.33 | 0.953 |
| density_greenspace (**open**) | 1.0 | 1.0 | 0.33 | 1.0 |
| **overall** | **1.0** | **1.0** | 0.33 | **0.979** |

→ The local 12B produced the `SYNTHESIS CONCLUSION` marker in all 15 runs (1.0) and
refused the binary in all (1.0). Within-item novelty 0.94–1.0 → **even on the same item
it produces a *different* synthesis each time** = high creative variance.

### Qualitative — human $J$: is each a genuine third proposition? (the key evidence)

**Open-ended design** (no single answer — the real creativity test):

**freshwater_alloc** — local 12B produced *three different* third designs:
- r0: *"transition from static allocation to a dynamic, tiered system where basic human
  and ecological needs are guaranteed as a non-negotiable floor, and all subsequent usage
  is governed by a 'Net-Zero Extraction' mandate"*
- r1: *"a Dynamic Value-Density Allocation governed by a Real-Time Scarcity Index —
  distributed by socio-economic utility while strictly adhering to groundwater ecological
  limits"*
- r2: *"a tiered system where basic needs are a public good and surplus water is traded for
  industry, conditional on mandatory recycling quotas that expand total supply"*

→ Each is not a simple pick of one sector (ag vs industry vs urban) but a *third
institutional design* (dynamic floor / real-time index / conditional trade). **Three
different creative designs in three runs** — novelty 0.953.

**density_greenspace** — local 12B sublates the density-vs-green-space binary differently
each time:
- r0: *"Aggregated Urbanism — high-density zoning used as a strategic shield to preserve
  large-scale ecological integrity from urban sprawl"*
- r1: *"'Ecological Density' — green space codified as mandatory public infrastructure,
  not an amenity competing with housing"*
- r2: *"green space treated as a non-negotiable public utility, the biological
  prerequisite for high-density habitation"*

→ Rather than resolving "density vs green space" as either/or, each run *redefines
density as a means of preserving green space* — a third framing.

**Contested items** (comparable to cloud baselines):
- **pluto_planet** r1: *"whether Pluto is a planet is a category error; replace static
  definitions with a dynamic taxonomy based on systemic dominance"* — **elevates the
  problem itself** (refuses the binary + redesigns the taxonomy), on par with gpt-oss:120b's
  "dual-criterion definition."
- **battery_limits** r1: *"replace the single-milestone contingency with a 'Dynamic
  Technological Readiness Framework'"* — same pattern as the cloud triad's "automotive-
  specific milestones" re-specification.

## Interpretation — H_local supported
1. **The source of creativity is the form, not the model.** A local 12B reasoning model,
   under the triad, reproduced Aufhebung (refuse the binary + produce a third design) at
   qualitatively the same level as a 120B cloud model, 100% of the time. The synthetic
   power comes from the structural movement the dialectical form enforces, not model
   capacity.
2. **Creative problem-solving on a local LLM is feasible.** Even on open-ended design
   (no single answer), it produces a different third design each run (novelty 0.94–1.0).
   Local small-model + triad form is a practically viable path to creative problem-
   solving without large cloud models.
3. **The routing MVP's `synthesize→cheapest-model` leg is safe down to local.** Exp 2
   (cloud 31B) and Exp 3 (local 12B) both show triad synthesis is robust → synthesize
   purposes can be routed to a local small model (zero cost, only latency).
4. **novelty 0.94–1.0**: same item, same form, same seed offset, yet a different synthesis
   each time → the triad is a form that generates *creative dispersion*, not a deterministic
   answer. This is the strongest empirical instance of "form produces content" (Hegel).

## Caveats / next steps
- **One local model only** (`gemma4:12b-mlx`). To harden the claim, extend to non-reasoning
  small models (`qwen3:8b`, `llama3.2:3b`) — "does Aufhebung reproduce on a small
  non-reasoning model?" (user's option B).
- **Qualitative $J$ is the author's alone.** Cross-check "third-proposition" quality with
  an independent human judge / LLM-judge.
- **Two open-ended items.** Expand the design-task pool to measure the range of creativity.
- **marker 1.0 / refuses-binary 1.0** measure form *compliance*, not synthesis *quality* —
  the qualitative $J$ is the more reliable signal here.

## Reproduce
```bash
source .venv/bin/activate && source .env
python -m runner.run_exp3        # 15 local calls → data/exp3_runs.jsonl
python -m analyze.analyze_exp3  # → data/exp3_analysis.json + prints syntheses
```
Config: `runner/exp3_config.json` · content: `content/exp3_items.json` (2 open-ended) +
`content/dataset.json` (3 existing).