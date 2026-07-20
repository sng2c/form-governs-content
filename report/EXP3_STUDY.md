# Exp 3 — Dialectical Triad Aufhebung Verified on a Small Local Model

> 한국어 버전: [`EXP3_STUDY.ko.md`](EXP3_STUDY.ko.md) · Experiments index: [`../EXPERIMENTS.en.md`](../EXPERIMENTS.en.md)
> **v0.3.0 reading**: Aufhebung reproducing down to 1B non-reasoning *dissolves* the "needs large/reasoning model" control (phantom) and *confirms* creativity-is-form-driven. The 1B novelty-cheat risk raises the $\alpha$ candidate control. Canonical view: [`CONTROL_PANEL.en.md`](CONTROL_PANEL.en.md).

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
  **within-item novelty (`within_item_novelty`: mean shingle distance across 3 repeats of the
  same model on the same item = repetition dispersion)**. **Key = human $J$**: qualitative
  judgment that each synthesis is a genuine third proposition, not a simple sum of the poles.

> ⚠️ **Novelty-definition caveat**: Exp3's novelty is **within-item (repetition dispersion)**.
> Exp2's `synth_novelty` in `mvp_analysis.json` is **cross-model (distinctiveness vs other
> models' conclusions)** — a different definition, not directly comparable. Do not place
> this experiment's `gemma3:1b` 0.995 (a different abstract phrasing each repeat) on the same
> axis as Exp2 `gpt-oss:120b` 0.894 (distinctiveness vs other models) and conclude "local 1B
> beats cloud 120B at creativity" — these are different quantities. Exp3 novelty measures
> "does the form generate a different synthesis each time," not "how original vs other models."

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

## ⚑ Exp 3b — extended to non-reasoning small models (option B done)
`gemma4:12b-mlx` was a reasoning model, so to test whether Aufhebung comes from the *form* rather than *reasoning capability*, two **non-reasoning small models** were added (llama3.2:3b, gemma3:4b; triad fixed; same 5 items × 3 repeats = 30 local calls).

### Cross-model quantitative
| model | kind | marker | refuses_binary | third-words | novelty |
|---|---|---|---|---|---|
| gemma4:12b-mlx | reasoning | 1.0 | 1.0 | 0.4 | 0.979 |
| **gemma3:4b** | **non-reasoning** | **1.0** | **1.0** | 0.33 | 0.965 |
| **llama3.2:3b** | **non-reasoning** | **0.8** | **1.0** | 0.27 | 0.983 |

### Key finding — Aufhebung reproduces without reasoning
1. **refuses_binary = 1.0 in all three** (reasoning, non-reasoning, 3B small). The triad's core Aufhebung property (refuse the binary) comes **from the form, not reasoning**. Even a 3B non-reasoning model refuses the binary in every run.
2. **novelty 0.96–0.98 in all** — creative dispersion is reasoning-independent; the 3B non-reasoning model still produces a *different* synthesis each run (0.983).
3. **Form *compliance* (exact marker emission) is capacity-sensitive**: gemma4 (12B reasoning) and gemma3 (4B non-reasoning) hit 1.0, but **llama3.2:3b drops to 0.8** (occasionally leaking raw `**THESIS` template text and missing the marker). → structural *compliance* is capacity-sensitive, but the dialectical *movement* (refuse binary + produce a third design) is form-driven and robust.
4. **Qualitative (human J)** — the 4B non-reasoning (gemma3:4b) produces genuine third designs: freshwater "tiered system + dedicated backstop fund", pluto **a third category "major dwarf planet"** (refuses the planet/dwarf binary + invents a new category), density "layered approach integrating density with ecologically-rich public space". The 3B (llama3.2:3b) also produces third designs (minimum_wage: "inflation-indexed, sector-specific, with caution") though marker omission is more frequent.

→ **H_local strengthened**: the source of creativity is the form, not reasoning. Aufhebung reproduces *fully* (marker 1.0) on a 4B non-reasoning model and *substantively* (marker 0.8 but refuses_binary 1.0, novelty 0.98) on a 3B. **Creative problem-solving via the triad is practically feasible on a local non-reasoning small model (3–4B) — no reasoning stage, no large model needed.**

## ⚑ Exp 3c — ultra-small 1B non-reasoning models (option C)
Option B reached non-reasoning 3–4B. To find the floor, two **1B-class non-reasoning** models (`llama3.2:1b`, `gemma3:1b`) were added (triad fixed; same 5 items × 3 repeats = 30 local calls).

### 5-model cross quantitative (75 runs total)
| model | kind | marker | refuses_binary | third-words | novelty |
|---|---|---|---|---|---|
| gemma4:12b-mlx | reasoning | 1.0 | 1.0 | 0.4 | 0.979 |
| gemma3:4b | non-reasoning | 1.0 | 1.0 | 0.33 | 0.965 |
| **gemma3:1b** | **non-reasoning 1B** | **1.0** | **1.0** | **0.73** | **0.995** |
| llama3.2:3b | non-reasoning | 0.8 | 1.0 | 0.27 | 0.983 |
| **llama3.2:1b** | **non-reasoning 1B** | **0.933** | **1.0** | **0.73** | 0.958 |

### Key — Aufhebung reproduces at 1B (the strongest H_local evidence)
1. **refuses_binary = 1.0 in both 1B models.** Even a 1B non-reasoning model refuses the binary every run. → the core of Aufhebung comes from the form, not reasoning or capacity.
2. **marker compliance**: `gemma3:1b` is **1.0** (a 1B model outperforming the 3B llama), `llama3.2:1b` 0.933 (only 1 of 15 runs missed the marker). → **form compliance is not monotonic in size**: the Gemma family follows the form better than Llama at equal size; it is family/quantization dependent, not purely size.
3. **novelty 0.958–0.995 at 1B** — creative dispersion holds at 1B; a different synthesis each run.
4. **third-word count 0.73 at 1B** — *higher* than at 3–4B (0.27–0.33). Smaller models lean more heavily on the template's "not X but Y / reframe / shift" phrasing (form-dependence *increases* as capacity drops).
5. **Qualitative (human J)** — 1B produces *named* third systems: `gemma3:1b` freshwater **"Dynamic Adaptive Allocation System — participatory, ecologically-informed, socially just"**, density **"a dialectical process where political mobilization (parks) and ecological regeneration (green-space creation) are mutually reinforcing"** (explicitly dialectical!), pluto "a revised definition prioritizing dynamic orbital stability, active geology, self-sustaining formation". `llama3.2:1b` freshwater **"Water Stewardship Model"**, pluto "a revised definition balancing clear orbital paths with gravitational interactions, elevating Pluto's status".

→ **H_local final support**: **the triad's Aufhebung reproduces even on a 1B non-reasoning ultra-small model** (refuses_binary 1.0, marker 0.93–1.0, novelty 0.96–0.995, named third designs produced). **Creative problem-solving via the triad is practically feasible on a local ultra-small (1B, non-reasoning) LLM — no reasoning stage, no large model, no cloud needed.** Creativity arises from the structural movement of the dialectical form, not from model capacity.

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