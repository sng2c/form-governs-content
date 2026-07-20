# Control Panel Spec — `pruner-dialectic` (formalization of the v0.3.0 discovered mechanism)

> 한국어: [`CONTROL_PANEL_SPEC.md`](CONTROL_PANEL_SPEC.md) · Canonical view: [`CONTROL_PANEL.en.md`](CONTROL_PANEL.en.md)
> This document formalizes the interface of the control panel *discovered* (not designed)
> by the Pruner v0.3.0 descent. $I_0$ (full automation) is confirmed phantom; the two
> surviving controls (`intent`, $\alpha$) resisted dissolution (real), so we now specify
> their interface.

## 0. Contract
> **Full automation, except two surgical human gates — each exposed only when its own
> trigger fires.** The goal is not full automation; it is *minimal, surgical human
> control*. Most runs expose 0 controls.

## 1. Automated core (no exposed controls)
```
(P, C) → [form binding] → [model routing] → [run M(F,C)] → S3 → [proxy compute m,ρ,ν,κ_op]
```
- **Form binding** (fixed, Exp1/2): `decide→red_blue_debate` · `synthesize→dialectical_triad` · `surface_assumptions→socratic_dialogue`.
- **Model routing** (matrix, Exp2/3): `synthesize/surface→cheapest local (gemma3:1b/4b)` · `decide-clear→cheap` · `decide-contested→reasoning (gpt-oss)` (varies under `intent`).
- **Proxies**: $m, \rho, \nu, \kappa_{\text{op}}$ auto-computed. *Narrowing only* — Stage B showed G/C are inseparable, so proxies never decide.

## 2. Control #1 — `intent` (bias-direction switch)
| field | value |
|---|---|
| trigger | $P=\text{decide}$ AND contestedness $r(C)\ge\theta_r$ |
| human input | `{scrutinize (conservative, lean no) \| include (incremental, lean yes) \| neutral}` |
| effect | route to the model/stance matching the chosen bias |
| hidden when | not decide, or $r<\theta_r$ → auto `neutral` |
| why human | a value judgment with no correct answer (Exp2: model-specific support/oppose) |

## 3. Control #2 — $\alpha$ (authenticity gate)
| field | value |
|---|---|
| trigger | $S_3$ in the low-operational-concreteness zone — $\kappa_{\text{op}}\le3.7$ (**kop-only**; ν dropped per Stage B — ν is non-discriminating). **α is scoped to `synthesize`** (decide uses `intent`; surface currently ungated) |
| human input | $S_3$ + observables + comparison → `G (genuine sublation) \| C (cheat) \| B (borderline)` |
| effect | G→accept · C→re-route to a stronger model / re-run · B→human decides |
| hidden when | clear case (proxies agree / unflagged) → auto-accept |
| why human | observables cannot separate G/C (Stage B: 18 indistinguishable pairs, logistic 0.625) — irreducible judgment |

## 4. Thresholds (data-grounded seeds)
- **$\theta_r \approx 0.30$** — from Exp1 verdict divergence: `battery 0.20 · pluto 0.225 < 0.30 < minimum_wage 0.425`. → only min_wage triggers `intent`; battery/pluto stay automated.
- **$\alpha$ borderline zone** — from Stage A: $\nu\ge0.999$ AND $\kappa_{\text{op}}\le3.7$.
- Both are *seeds*; calibrable on the preserved raw (option 3 done).

## 5. Minimization (how the panel shrinks)
| run type | exposed controls |
|---|---|
| synthesize / surface (majority) | **0** |
| decide-clear | 0 |
| decide-contested (e.g. min_wage) | **intent** |
| any P, $S_3$ borderline flag | **$\alpha$** |
| decide-contested + $S_3$ borderline (rare) | **intent + $\alpha$** |

## 6. Evidence basis (which experiment fixed each piece)
- form governs content → **Exp1** (verdict divergence 0.283).
- model routing mostly dissolves (synthesize/surface model-independent) → **Exp2/3** (1B robust).
- `intent` real (decide-contested verdict model-dependent) → **Exp2** (min_wage support/oppose split).
- $\alpha$ candidate raised (1B novelty-cheat risk) → **Exp3**.
- $\alpha$ real (not dissolvable into observables) → **Stage B** (human labeling).
- $I_0$ (full automation) phantom confirmed → **Stage B** ($\alpha$ non-dissolvable ⇒ full automation impossible).

## 7. Status
- v0.3.0 **termination reached**: both controls resist dissolution (real); no phantom control left to delete.
- This spec formalizes the interface of the *discovered* control panel. Implementation (automated core + gate-exposure logic) is the next step.

## 8. Unimplemented (formalization limit)
- The routing matrix and proxy computation are coded (`runner/`, `analyze/`), but the
  *gate-exposure logic* (showing intent/α to a human and taking input when triggered) is
  not yet built. This spec is the contract for that implementation.