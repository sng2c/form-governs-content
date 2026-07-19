# MVP Study — Running the Purpose→Template Binding Across Model Types

> 한국어 버전: [`MVP_STUDY.ko.md`](MVP_STUDY.ko.md) · Main report: [`REPORT.md`](REPORT.md)

Follow-up experiment run after approving the Pruner (MVP) compromise. With **$\Phi$
(ideal-template generation) kept a black box**, the linear spine (purpose→bind→run) was
exercised across **8 model types** on Ollama Cloud, and we ask how "form governs content"
varies with model type.

## Design (MVP linear spine)
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

→ The **linear spine is robust to model type**: nearly every model follows the structural
requirements of the dialectical form (markers/sections). Only general-moe (kimi/qwen)
occasionally drops a marker (0.75/0.875). "Form governs structure" is largely model-independent.

### 2. But form's governance of the *verdict* is model-dependent
**`minimum_wage / decide` (red_blue_debate)** — same form, models split:
| model | verdict |
|---|---|
| gpt-oss:120b | **support** |
| kimi-k2.6 | **support** |
| minimax-m3 | **support** |
| qwen3.5:397b | **support** |
| gemma4:31b | **oppose** — "1.3M job loss offsets poverty-reduction gains, validating neoclassical concerns" |
| deepseek-v4-flash | **oppose** — "projected job losses significant, empirical literature mixed" |
| glm-5.2 | **oppose** — "equal trade-off of 1.3M lifted vs 1.3M jobs lost" |
| mistral-large-3:675b | **qualified** — "evidence favors a moderate increase, but a $15 national mandate is too high" |

→ **On the same contested content under the same red/blue form, the verdict splits by
model**: gpt-oss/kimi/minimax/qwen → support; gemma/deepseek/glm → oppose. By contrast, on
the clearer item `pluto_planet`, 7/8 models converge on "reclassify" (yes) — only mistral
is mixed.

⇒ **Form governs structure model-independently, but the verdict is model-dependent on
contested items** — which is exactly why $\Phi$ was left a black box: a single bound
template cannot guarantee the *correct* verdict across all models. The **human-$J$ gate
remains necessary on contested items**.

### 3. Aufhebung (synthesis) is reproduced across all model types (H1a)
New-proposition rate for `synthesize / dialectical_triad` (shingle novelty vs other models' conclusions):
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
- Note: the non-thinking small model gemma commits to the most decisive "oppose" under
  `decide` — **less reasoning ⇒ more exposed to the form's binary structure (red/blue)**,
  while thinking models hedge.

## Interpretation — validating the MVP design bet
1. **The linear spine holds**: purpose→bind→run realizes the form's *structure* stably
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