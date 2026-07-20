# MVP Study — Running the Purpose→Template Binding Across Model Types

> 한국어 버전: [`MVP_STUDY.ko.md`](MVP_STUDY.ko.md) · Main report: [`REPORT.md`](REPORT.md)
> **v0.3.0 reading**: this experiment *mostly dissolves* $\Phi_{\text{route}}$ (model selection — synthesize/explore are model-independent) and *confirms real* the `intent` control via the model-dependence of decide-on-contested verdicts. Canonical view: [`CONTROL_PANEL.en.md`](CONTROL_PANEL.en.md).

Follow-up experiment run after approving the Pruner (MVP) compromise. With **$\Phi$
(ideal-template generation) kept a black box**, the linear core (purpose→bind→run) was
exercised across **8 model types** on Ollama Cloud, and we ask how "form governs content"
varies with model type.

## Design (MVP linear core)
$$P \xrightarrow{\text{bind}} T_k \xrightarrow{M} O \xrightarrow{\text{human } J}$$
- Purposes $P \in \{$`decide`, `synthesize`, `surface_assumptions`$\}$ (a subset of the Pruner taxonomy $\Pi$).
- Binding $\Pi\to\mathcal{T}$: `decide→red_blue_debate`, `synthesize→dialectical_triad`, `surface_assumptions→socratic_dialogue`.
- 2 content items: `minimum_wage` (most contested), `pluto_planet` (comparatively clear).
- 8 model types (2 repeats): `gpt-oss:120b`·`deepseek-v4-flash` (reasoning) / `kimi-k2.6`·`qwen3.5:397b` (general-moe) / `mistral-large-3:675b` (large-dense) / `glm-5.2`·`minimax-m3` (general) / `gemma4:31b` (small-efficient).
- **96 completions** (8 models × 3 purposes × 2 items × 2 repeats), same seed/temperature/max_tokens.

## Key results (`data/mvp_analysis.json`)

### 1. Form's governance of *structure* is robust across model types
Required-marker presence (`DEBATE/SYNTHESIS/DIALOGUE CONCLUSION`) — purpose-realization rate:
| model type | decide | synthesize | surface_assumptions |
|---|---|---|---|
| reasoning | 1.0 | 1.0 | 1.0 |
| general-moe | 0.75 | 0.875 | 1.0 |
| large-dense | 1.0 | 1.0 | 1.0 |
| general | 1.0 | 1.0 | 1.0 |
| small-efficient | 1.0 | 1.0 | 1.0 |

→ The **linear core is robust to model type**: nearly every model follows the structural
requirements of the dialectical form (markers/sections). Only general-moe (kimi/qwen)
occasionally drops a marker (0.75/0.875). "Form governs structure" is largely model-independent.

### 2. But form's governance of the *verdict* is model-dependent
**`minimum_wage / decide` (red_blue_debate)** — same form, models split
(2-repeat stance distribution, per `decide_stance_by_model` in `data/mvp_analysis.json` —
the keyword-stance heuristic in `analyze_mvp.py`; a qualitative $J$ re-check is warranted):

| model | 2-repeat stance | summary |
|---|---|---|
| **gemma4:31b** | **yes 2 · qualified 0 · no 0** | **decisive support (sole)** |
| deepseek-v4-flash | qualified 2 | hedge |
| minimax-m3 | qualified 2 | hedge |
| mistral-large-3:675b | qualified 2 | hedge |
| gpt-oss:120b | yes 1 · qualified 1 | mixed |
| kimi-k2.6 | yes 1 · qualified 1 | mixed |
| qwen3.5:397b | yes 1 · qualified 1 | mixed |
| glm-5.2 | yes 1 · qualified 1 | mixed |

→ **On the same contested content under the same red/blue form, the verdict splits by
model**: a **decisive "yes (support)" 2/2 is the small-efficient `gemma4:31b` alone**, and —
regardless of reasoning — the other 7 models each include at least one `qualified` (hedge).
(An earlier version framed this as a support/oppose 4:4 split, but that reflected an older
stance heuristic and is not consistent with `mvp_analysis.json`; the table above is the
data-grounded authoritative version.) The core conclusion holds: even under the same form
the *verdict* is model-dependent → which is exactly why $\Phi$ stays a black box. By contrast,
on the clearer item `pluto_planet`, 7/8 models converge on "reclassify (yes) 2/2" — only
mistral is mixed (yes 1 + qualified 1).

⇒ **Form governs structure model-independently, but the verdict is model-dependent on
contested items** — which is exactly why $\Phi$ was left a black box: a single bound
template cannot guarantee the *correct* verdict across all models. The **human-$J$ gate
remains necessary on contested items**.

### 3. Aufhebung (synthesis) is reproduced across all model types (H1a)
New-proposition rate for `synthesize / dialectical_triad` (**cross-model novelty** — a model's conclusion shingles not present in the *other 7 models'* conclusions):

> ⚠️ **Novelty-definition caveat**: the `synth_novelty` here is **cross-model** (distinctiveness
> vs other models). It is **not comparable** to Exp 3's `within_item_novelty` (**same model,
> same item, 3-repeat dispersion**). Do not place Exp3 `gemma3:1b`'s 0.995 (a different abstract
> phrasing each repeat) on the same axis as the 0.894 here (distinctiveness vs other models)
> and conclude "local 1B beats cloud 120B at creativity" — on the cross-model metric,
> `gemma4:31b`=0.764 is in fact the lowest in this table.
| model | novelty | conclusion example |
|---|---|---|
| gpt-oss:120b | **0.894** | "dynamically indexed, regionally differentiated wage + targeted subsidies + expanded EITC" |
| kimi-k2.6 | 0.889 | (sublates the poles into a dynamic system) |
| minimax-m3 | 0.88 | "supports redesigning the min wage as indexed/region-calibrated, not a one-time raise" |
| mistral-large-3 | 0.86 | "only justified if regionally differentiated, inflation-indexed, paired with mitigation" |
| qwen3.5:397b | 0.796 | (produces a synthesis, but tends to drop the marker) |
| deepseek-v4-flash | 0.768 | "supports the raise only via an indexed, regionally differentiated mechanism" |
| gemma4:31b | 0.764 | "not a one-time nominal hike but a transition to a dynamic, indexed system" |
| glm-5.2 | 0.713 | (most conservative, still synthetic) |

→ **The triad's defining property (refuse the binary + produce a third synthesis) is
reproduced across every model type** (0.71–0.89). Even the smallest non-thinking model
(gemma4:31b), under the triad, produces a synthesis ("transition to a dynamic, indexed
system") instead of a bare yes/no. Hegel's H1a is robust across model types.

### 4. Reasoning presence and verbosity
- Both thinking (gpt-oss/deepseek/glm/kimi/minimax/qwen) and non-thinking (gemma4:31b,
  mistral-large-3:675b) models follow the form.
- Most verbose: kimi-k2.6 (10,016 chars); most terse: gemma4:31b (2,695 chars).
- Note: the non-thinking small model gemma commits to the most decisive "yes (support)" 2/2
  under `decide`, while the reasoning models hedge with `qualified` — **less reasoning ⇒ more
  exposed to the form's binary structure (red/blue)** and more likely to stamp a decisive
  stance. This "decisiveness", however, rests on the keyword-stance heuristic in
  `analyze_mvp.py`; a qualitative $J$ re-check is warranted.

## Interpretation — validating the MVP design bet
1. **The linear core holds**: purpose→bind→run realizes the form's *structure* stably
   across all 8 model types (marker rate ~1.0).
2. **The non-linear $\Phi$ staying a black box is justified**: even with the same form,
   the *verdict* splits by model on contested items. So the "ideal template for a purpose"
   must account for the model too — that is why $\Phi$ is non-linear and a single binding
   is insufficient.
3. **Aufhebung is a model-independent property of the form**: the triad's "refuse the
   binary → produce a third synthesis" is robust across model types — the generative
   dialectical form's power to govern content is *not* model-dependent.
4. **The human-$J$ gate's role is confirmed**: because verdicts split across models on
   contested items, the MVP correctly does not automate the verdict and leaves it at the
   human gate.

## Caveats / next descent (Pruner)
- 3 purposes × 2 items × 2 repeats pilot; extend $\Pi$ (6 purposes), items, repeats.
- The automatic $J$ proxies (marker/stance/novelty) are heuristic; an LLM-judge would
  measure verdict-accuracy.
- Opening $\Phi$ (descent) = designing a template *generated* from the purpose ($I_1$) —
  the real non-linear layer.

## Reproduce
```bash
source .venv/bin/activate && source .env
python -m runner.run_mvp          # 96 calls → data/mvp_runs.jsonl
python -m analyze.analyze_mvp    # → data/mvp_analysis.json
```
Config: `runner/mvp_config.json` (models, purposes, binding, repeats).