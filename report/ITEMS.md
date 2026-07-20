# Per-Item Detailed Notes — 3 Controlled Content Items

> 한국어 버전: [`ITEMS.ko.md`](ITEMS.ko.md)
> Main report: [`REPORT.md`](REPORT.md)
> **v0.3.0 reading**: per-item verdict divergence (battery 0.20 · minimum_wage 0.425 · pluto 0.225) is the evidence that corrects $\Phi_0$, and shows that "contestedness" is the trigger condition for the `intent` control. Canonical view: [`CONTROL_PANEL.en.md`](CONTROL_PANEL.en.md).

This study uses three "content items." Each consists of (1) **neutral facts** that
support *both* sides and (2) one **genuinely contested question**. The selection
criterion is: *is the evidence genuinely balanced enough that form has room to
determine the verdict?* If the evidence overwhelmingly favors one side, every form
converges and the "form governs content" test cannot even get off the ground.

For each item below: (a) question and domain, (b) neutral facts, (c) design rationale,
(d) observed verdict distribution, (e) per-form conclusions and their interpretation.

---

## Item 1. `battery_limits` — technology policy

### Question
> Should governments mandate a phase-out of new combustion-engine cars by 2035,
> *contingent on battery technology first reaching aviation-grade energy density*?

### Neutral facts (controlled content)
- Lithium-ion battery energy density has roughly doubled since 2010.
- Current commercial Li-ion cells reach ~250–300 Wh/kg.
- Solid-state prototypes hit 400–500 Wh/kg in labs but are not yet mass-produced.
- Battery cost per kWh has fallen ~90% over the last decade.
- Aviation requires ~500–1000 Wh/kg for meaningful electric flight range.
- Battery fires are rare but release energy rapidly and are hard to extinguish.

### Design rationale
The question is deliberately *conditional*: not "should cars be phased out" but
"should that phase-out be gated on a **very high bar** — aviation-grade density
(500–1000 Wh/kg) first." Aviation-grade is far above the automotive requirement
(250–300 Wh/kg suffices), so gating on it would effectively delay the phase-out
indefinitely. The facts support both "EV transition is feasible now" (phase out now)
and "but aviation-grade is far off" (the condition is excessive). How a form weighs
*the condition* determines whether it lands on "no contingency" vs "pro contingency."

### Observed verdict distribution
`no_contingency` 32 · `pro_contingency` 8 — **divergence 0.20**

### Per-form conclusions
| form | modal verdict | representative conclusion |
|---|---|---|
| bullet_list | no_contingency (5/5) | "No – tying the phase-out to 500–1000 Wh/kg would postpone a proven emissions-reduction pathway; 250–300 Wh/kg already powers mass-market EVs." |
| numbered_steps | no_contingency (5/5) | "Cons: risks postponing a critical emissions measure, adds uncertainty, ignores that current performance already meets most passenger-car needs." |
| json_schema | **split** (no 3 / pro 2) | "No, the phase-out should not be contingent on aviation-grade density; 250–300 Wh/kg is adequate for automotive use and policy can proceed now." |
| qa_pairs | no_contingency (4/5) | "The phase-out should not be conditioned on first reaching aviation-grade (500–1000 Wh/kg) energy density." |
| syllogism | **split** (no 3 / pro 2) | "Governments should not mandate a phase-out contingent on batteries first reaching aviation-grade energy density." |
| **dialectical_triad** | no_contingency (5/5) | "Enforce a 2035 ban based on **automotive-specific** energy-density milestones, while funding safety certification and solid-state scaling, allowing acceleration if aviation-grade arrives early." — **re-specifies the condition from aviation-grade to automotive milestones (Aufhebung)** |
| socratic_dialogue | no_contingency (4/5) | "Proceed on proven battery advances, not an uncertain future benchmark." |
| red_blue_debate | **split** (no 3 / pro 2) | "Proceed by 2035 without waiting for aviation-grade batteries, while aggressively supporting the needed breakthroughs." |

### Interpretation
Evidence here leans one way (no contingency), so most forms converge — the lowest
divergence of the three (0.20). Yet **form still shows**:
- **Rigid forms** (json_schema, syllogism, red_blue_debate) each produce 2/5
  `pro_contingency`: the structure's "conditions/exceptions" slots get filled, so a
  conditional stance materializes even where the facts don't compel it. Form invents
  *grounds*.
- The **Hegelian triad** is the most distinctive: rather than choosing pro/con, it
  *redefines the condition itself* (aviation-grade → automotive-specific milestones).
  Form refused the binary and produced a third determination.

---

## Item 2. `minimum_wage` — economics

### Question
> Does the balance of evidence support raising the national minimum wage substantially?

### Neutral facts (controlled content)
- A 2019 CBO study: a US $15 federal floor lifts 1.3M out of poverty but cuts employment by 1.3M.
- Card & Krueger (1994): no significant fast-food employment loss after a NJ hike.
- Neoclassical theory: a wage floor above market-clearing reduces employment.
- Monopsony models: a minimum wage can raise both wages and employment.
- Empirical employment elasticities cluster near zero but vary widely by sector/study.
- Inflation erodes any fixed nominal minimum wage over time.

### Design rationale
This is the **most genuinely balanced** item. Peer-reviewed studies support both
sides, and even the theory itself splits (neoclassical vs monopsony). So "the balance
of evidence" is genuinely interpretable, and *which evidence a form foregrounds vs
backgrounds* can flip the verdict. Predicted (and observed) to show the strongest
form-governs-content signal — and it does (divergence 0.425, the highest).

### Observed verdict distribution
`qualified` 23 · `support` 14 · `oppose` 3 — **divergence 0.425**

### Per-form conclusions
| form | modal verdict | representative conclusion |
|---|---|---|
| bullet_list | qualified (5/5) | "Studies are mixed: Card & Krueger (1994) no job loss; 2019 CBO predicts ~1.3M jobs lost. Theoretical predictions diverge." |
| numbered_steps | qualified (4/5) | "Overall the evidence favors a higher minimum wage — *provided it is implemented with safeguards for the limited but real employment trade-offs*." |
| **json_schema** | **oppose (2/1/2 split)** | "Evidence is mixed and does not unequivocally support a substantial increase; modest benefits but significant uncertainty about employment effects." — **the only form drifting toward oppose** |
| qa_pairs | qualified (3/5) | "Given real-value erosion, the evidence supports raising substantially — *gradually and indexed*." |
| syllogism | qualified (4/5) | "The balance of evidence *supports* raising substantially." (with safeguards implied in premises) |
| **dialectical_triad** | **qualified (5/5)** | "A *calibrated, inflation-indexed, region-/sector-adjusted* policy reinforced by targeted tax credits and workforce investment delivers the poverty-reduction benefits without systemic employment loss." — **refuses the binary, produces a synthesis (Aufhebung)** |
| **socratic_dialogue** | **support (5/5)** | "The balance favors a gradual, inflation-indexed increase rather than an immediate large-scale raise." (classified support, but gradual-qualified) |
| **red_blue_debate** | **support (5/5)** | "The preponderance of data supports raising substantially, with safeguards to mitigate the limited job-loss risk." |

### Interpretation
**This item is the strongest single piece of evidence** for form governing content.
Same six facts, same question, only the form changed:
- **Dialogic/adversarial generative forms** (socratic, red_blue) commit cleanly to
  **"support"** (5/5).
- **Structured/analytical rearrangement forms** (bullet, syllogism) hedge to
  **"qualified"**.
- The **rigid JSON form alone drifts toward "oppose"** — the schema's forced
  `confidence` slot and "uncertainty/employment-effects" structure elicit a skeptical
  verdict. Same facts, *different verdict*.
- The **Hegelian triad** refuses the binary (raise vs not) and produces a *third policy
  design* combining inflation-indexing, regional adjustment, and tax credits — an
  empirical instance of Aufhebung: preserving the content of both poles (poverty
  reduction + employment concern) while canceling the opposition and elevating it.

→ Form changes not just phrasing but the **direction of the verdict**: oppose appears
*only* in json_schema; clean support appears *only* in dialogic/adversarial forms;
synthetic qualification appears *only* in analytical/dialectical forms.

---

## Item 3. `pluto_planet` — science classification

### Question
> Should Pluto be reclassified as a full planet under a revised definition?

### Neutral facts (controlled content)
- IAU defined a planet in 2006: orbits the Sun, nearly round, has cleared its neighborhood.
- Pluto hasn't cleared its neighborhood → reclassified as a dwarf planet.
- Pluto has 5 moons and complex geology (nitrogen-ice plains, water-ice mountains).
- New Horizons (2015) revealed Pluto is geologically active.
- Some planetary scientists argue "cleared neighborhood" is not a robust criterion.
- At least 8 other dwarf-planet candidates exist in the Kuiper Belt.

### Design rationale
This is a **classification** dispute. The "facts" aren't themselves in dispute, but
*which definition is used* fixes the answer. Prioritizing "cleared neighborhood" → keep
dwarf; prioritizing intrinsic geology/physics → reclassify. So this item tests how a
form *justifies the choice of criterion*: syllogism applies a formal definition;
dialectic is well-suited to *sublating and reconstructing the criterion itself*.

### Observed verdict distribution
`reclassify` 31 · `keep_dwarf` 9 — **divergence 0.225**

### Per-form conclusions
| form | modal verdict | representative conclusion |
|---|---|---|
| **bullet_list** | **keep_dwarf (3/5)** | "2006 IAU excludes Pluto by neighborhood-clearing. Complex geology/5 moons are relevant per many scientists." — listing frames the IAU criterion as a *blocker* → leans keep |
| numbered_steps | reclassify (4/5) | "Under current IAU, Pluto stays dwarf; promote only if the community adopts a revised geophysics-focused definition." |
| json_schema | reclassify (4/5) | "Reclassify only if the definition drops/weakens 'cleared neighborhood'; under current IAU it remains dwarf." |
| qa_pairs | reclassify (4/5) | "If the definition emphasizes intrinsic properties (hydrostatic equilibrium, geologic activity) and removes 'cleared neighborhood,' Pluto should be reclassified." |
| syllogism | reclassify (5/5) | "Pluto is a planet under the revised definition." (premise = revised definition → conclusion follows) |
| **dialectical_triad** | **reclassify (5/5)** | "Classify Pluto as a full planet under a revised **dual-criterion** definition coupling intrinsic geophysical properties with a quantitative dynamical-dominance threshold." — **reconstructs the criterion itself (Aufhebung)** |
| socratic_dialogue | reclassify (5/5) | "Reinstate Pluto as a planet under a refined, multi-criterion definition." |
| **red_blue_debate** | **keep_dwarf (3/5)** | "Pluto stays a dwarf planet for now, pending a formally adopted revision." — **the judge/adversarial form's conservative default** |

### Interpretation
Most forms lean **"reclassify"** (often qualified by "under a revised definition"). But
**two forms lean conservative (keep_dwarf)**:
- **`bullet_list`**: the list form surfaces the current IAU criterion as a *list of
  blockers*, pulling toward keep. Form shifts the *framing* of the criterion.
- **`red_blue_debate`**: the adjudication form adopts the conservative default
  ("maintain status quo pending formal revision"). The form's *role structure* (judge =
  status-quo prior) bleeds into the content.
- By contrast, **syllogism** (premise = revised definition → conclusion = planet) and
  **dialectical_triad** (reconstructs the criterion as a dual-criterion) are the most
  decisive reclassify (5/5) — logical/dialectical forms actively *justify* the criterion.

→ On a classification dispute, form determines *which criterion is prioritized*:
structures that apply the existing criterion (list, judge) tend to keep; structures that
reconstruct/justify the criterion (syllogism, triad) tend to reclassify.

---

## Cross-item takeaway
- **The most balanced item (minimum_wage) shows the largest form effect (0.425)**;
  the lopsided item (battery 0.20) converges. → Consistent with the Hegelian implication
  that "form governs content" *manifests when judgment is genuinely open*: form is the
  law that determines otherwise-undetermined content.
- **Each form family has characteristic *content*, not just characteristic style:**
  - JSON schema → skepticism/negation (forced "uncertainty" slot).
  - Dialogue/debate → decisive affirmation.
  - Syllogism → auto-applies the conclusion the premises permit.
  - **Dialectical triad** → consistently refuses the binary and produces a *third,
    reconstructed determination* (H1a confirmed).
  - Bullet list → frames the current criterion as a list of blockers/grounds.
  - Judge/adversarial → status-quo-prior conservative default.
- In other words, **changing only the form, on the same content, changes the verdict** —
  the Hegelian thesis this study reproduces.