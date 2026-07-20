# Control Panel — form-governs-content re-aligned under Pruner v0.3.0

> 한국어: [`CONTROL_PANEL.md`](CONTROL_PANEL.md) · Pruner lens: `pruner-arch` v0.3.0
> This is the **canonical view** of the current deliverable. The experimental *data and
> measurements are unchanged*; only the interpretive frame is re-aligned to v0.3.0
> (regulative ideal · MVP = control panel · deleting phantom controls). Past session log:
> [`PRUNER_LOG.md`](PRUNER_LOG.md).

---

## 1. Regulative Ideal $I_0$ (existence not assumed)
**"A fully-automated, cost-zero, model-agnostic creative-synthesis pipeline"** — give it
a purpose + content and get a *genuine* creative synthesis, with no human, no large model,
no cloud.

$I_0$ is a **regulative ideal** (do not assume it exists). Dissolution testing has been
*downward-correcting* it:
- The "creative synthesis" part *dissolves* (form-driven, automatable).
- "Full automation" holds *only if* $\alpha$ (authenticity) dissolves. If $\alpha$ resists,
  $I_0$ (full automation) is a **phantom**, and the real deliverable is "automated core +
  minimal control panel".

## 2. Control-Panel (candidate controls) dissolution map
Every black box deferred in the session is re-read as a candidate control. Each was
tested on descent and classified **dissolved (phantom→delete) / resisted (real→keep) /
untested (frontier)**:

| candidate control (black box) | dissolution status | evidence (experiment) | panel disposition |
|---|---|---|---|
| $\Phi_0$: generate ideal template $T^*(P,M)$ | **dissolved** | form guarantees structure+synthesis model-independently (Exp1/2/3 marker 1.0, 1B Aufhebung) → template is *invariant* | **deleted (phantom)** |
| $\Phi_{\text{route}}$: select model $M^*(P)$ | **mostly dissolved** | synthesize/surface are model-independent (Exp3 1B OK) → absorbed into routing matrix (linear); residual = decide-on-contested verdict only (Exp2) | matrixed (auto); residual → `intent` |
| $\Psi$: optimal feature vector $F^*$ | **dissolved** | with template invariant, feature selection is moot → absorbed by $\Phi_0$'s dissolution | **deleted (phantom)** |
| `intent`: bias direction for decide-on-contested | **resisted (real)** | "which bias do you want" is a human value judgment, no automated correct answer (Exp2 observed model-specific support/oppose) | **kept (real, a switch)** |
| $\alpha$ ($J_{\text{auto}}$): synthesis authenticity (sublation vs novelty-cheat) | **untested (frontier)** | 1B emits high novelty that may be a cheat; $\alpha\approx f(m,\rho,\nu,\kappa_{\text{op}})$ residual unmeasured | **candidate, dissolution test pending** |
| $\Sigma$: sublation detection | folded into $\alpha$ | authenticity = sublation $\wedge$ concreteness | (not a separate control) |

## 3. Current MVP = current control panel (frozen)
After deleting phantom controls, the surviving panel:

**Automated core (dissolved/linear, no human control):**
$$P \xrightarrow{\text{fixed form}} F \xrightarrow{\text{routing matrix}} M \xrightarrow{\text{synthesis generation}} S_3$$
Robust down to 1B non-reasoning → cost 0, model-agnostic, already automated.
(Implementation: [`ROUTING.md`](ROUTING.md))

**Control #1 — `intent` (real, kept):** a switch choosing the bias direction
(conservative-scrutiny vs incremental-inclusion) for `decide` on contested items. Human
responsibility. Not automatable (no correct answer).

**Control #2 — $\alpha$ authenticity gate (candidate, untested):** whether $S_3$ is a
genuine sublation or a novelty-cheat. Proxies (novelty $\nu$, operational concreteness
$\kappa_{\text{op}}$) narrow candidates; a human disposes only on the borderline.
- **I/O contract:** input $(S_3, P, M, \text{observables } m,\rho,\nu,\kappa_{\text{op}})$ →
  output {authentic / borderline→human / not}.

> v0.3.0 in one line: this MVP *is* the current control panel. Phantom controls
> ($\Phi_0$, most of $\Phi_{\text{route}}$, $\Psi$) are deleted; the real one (`intent`)
> is kept; the candidate ($\alpha$) awaits a dissolution test. The panel shrinks by
> deleting phantom controls on descent.

## 4. $\alpha$ dissolution test result (Stage B, 24 human labels) — **RESISTS -> real**
Measured the residual of $\alpha \approx f(m,\rho,\nu,\kappa_{\text{op}})$ with human labels (G=2,B=1,C=0).
- Best single-threshold accuracy (G vs C) **0.625** (near chance); 4-observable logistic combo **0.625** — **all 6 G (1,2,14,16,19,23) misclassified**.
- Observationally-indistinguishable G/C pairs: **18** (G#1/#2, κ_op=0 ≡ C#4/5/6/10/11, κ_op=0).
- authenticity-vs-observable correlation: m=0.22, ν=0.12, κ_op=0.15 — all near zero.
- **Verdict**: $\alpha$ cannot be dissolved into observables → **kept as a real control** (human-responsibility gate). $I_0$ (full automation) **confirmed phantom**.
- What α measures (genuineness of a *new category / conceptual sublation*) is structurally beyond operational-verb density (κ_op) → irreducibly human.

## 5. v0.3.0 reading of each experiment (which control it dissolved/confirmed)
- **Exp1** (120, single model · 8 forms): form governs content (verdict divergence 0.283)
  → corrects the hidden assumption "$\Phi_0$: template is content-irrelevant" (form
  determines the verdict). The triad refuses the binary + produces a third → first
  evidence that creativity is form-driven.
- **Exp2** (96, 8 models · per-purpose): structure+synthesis of synthesize/surface are
  model-independent → $\Phi_{\text{route}}$ (model selection) *mostly dissolves*. Only
  decide-on-contested is model-dependent (support/oppose split) → `intent` control
  *confirmed real*.
- **Exp3** (75, 1–12B local · triad): Aufhebung reproduces down to 1B non-reasoning
  (refuses_binary 1.0, novelty 0.96–0.995) → the "needs large/reasoning model" control
  *dissolves* (phantom); creativity-is-form-driven *confirmed*. The 1B novelty-cheat risk
  raises the $\alpha$ *candidate control*.
- **ROUTING** (matrix): the implementation of the automated core + the `intent` control.
  Both the dissolved part of $\Phi_{\text{route}}$ and its resisting residual (intent) live
  there together.

## 6. Deliverable status (per v0.3.0)
- **Automated core**: implemented (ROUTING matrix + 1B local verification).
- **Control #1 `intent`**: confirmed real (Exp2) — decide-on-contested bias switch.
- **Control #2 $\alpha$**: **confirmed real** (Stage B — resisted dissolution) — synthesis authenticity gate.
- **$I_0$ (full automation)**: **confirmed phantom** (α does not dissolve, so impossible).
- **Control panel stable**: both controls resist dissolution → no phantom control left to delete → **the discovered practical mechanism = automated core + {intent, α} 2-control panel**. Full automation was never the goal; minimal, surgical human control is.