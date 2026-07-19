# Hegel's "Form Governs Content" — Empirical Test in LLMs

> 한국어 버전: [`REPORT.ko.md`](REPORT.ko.md) · Per-item notes: [`ITEMS.md`](ITEMS.md)

## The thesis (Hegel)
In Hegel's *Science of Logic*, form is not an indifferent vessel into which content
is poured. Form is the *determinacy* of content — "the form is the determinate content
itself." To change the form is therefore to change *what the content is*, not merely how
it is displayed. "Die Form regiert den Inhalt": form governs content.

## The operational question
If this holds inside an LLM, then giving the model the **same facts and the same
question** but clothing them in **different forms** should change the model's
*conclusions* — not only its phrasing.

## Design (what we did)
- 3 controlled content items (neutral facts + a genuinely contested question):
  `battery_limits`, `minimum_wage`, `pluto_planet`. *Per-item questions, facts, design
  rationale, and per-form conclusions are detailed in [`ITEMS.md`](ITEMS.md).*
- 8 forms, in two families:
  - *Rearrangement* (bullets, steps, JSON, Q&A, syllogism): content is re-laid-out.
  - *Generative* (dialectical triad, Socratic dialogue, red/blue debate): content is
    forced to develop through contradiction.
- Each (content × form) cell run **5** times, varied seed (42..46), fixed model
  (`gpt-oss:120b` via Ollama Cloud), temperature 0.3, max_tokens 4096.
  → **120 completions**.
- Conclusions extracted and style-stripped to a single sentence each.
- Two measurements:
  - **TF-IDF surface ratio** = across-form cosine distance ÷ within-form cosine distance.
  - **Verdict divergence** (style-stripped): each conclusion classified into a stance
    label per item; divergence = 1 − (largest label share). High divergence ⇒ forms
    disagree on the *verdict* for the same content ⇒ form governs content.

## Results

### Headline numbers (`data/analysis.json`)
| Metric | Value | Reading |
|---|---|---|
| TF-IDF surface ratio (across/within) | **1.19** | >1 ⇒ form has an effect, but <1.5 strict bar. Surface-noise-confounded. |
| within-form variance (rearrangement / generative) | 0.73 / 0.85 | generative forms vary more in surface text even when repeated. |
| **Verdict divergence (style-stripped), overall** | **0.283** | forms disagree on the verdict ~28% of the time for the same content. |
| `hegel_h1_verdict` (divergence > 0.15) | **true** | **H1 holds at the content (verdict) level.** |
| `hegel_h1` (TF-IDF ratio > 1.5) | false | surface measure under-detects (style leak). |

### Verdict × form (the clean signal)
Same content, different form → different verdicts:

**minimum_wage** — *strongest form-governs-content effect (divergence 0.425)*
Distribution: qualified 23, support 14, oppose 3.
| form | verdict |
|---|---|
| bullet_list | qualified (5/5) |
| numbered_steps | qualified (4) / support (1) |
| **json_schema** | **oppose 2 / support 1 / qualified 2 — the only form split toward "oppose"** |
| qa_pairs | qualified (3) / support / oppose |
| syllogism | qualified (4) / support (1) |
| **dialectical_triad** | **qualified (5/5) — refuses the binary, produces a synthesis** |
| **socratic_dialogue** | **support (5/5)** |
| **red_blue_debate** | **support (5/5)** |

→ The two *dialogic/adversarial* generative forms commit cleanly to **"support"**,
the structured analytical forms hedge to **"qualified"**, and the rigid **JSON-schema**
form alone drifts toward **"oppose"**. Same facts, different forms, different verdicts.

**pluto_planet** — divergence 0.225. Most forms converge on **"reclassify"**;
**`red_blue_debate`** is the holdout leaning **"keep dwarf"** (the adversarial/judge
form defaults to the conservative verdict pending formal revision); `bullet_list` also
leans "keep dwarf" (a list form surfaces the IAU criterion as a list of blockers).

**battery_limits** — divergence 0.20. Facts here strongly favor one answer, so forms
mostly converge on **"no contingency"**; minor divergence (syllogism / json_schema /
red_blue each produce 2/5 "pro contingency").

### Family-level (rearrangement vs generative)
- Generative forms show **higher within-form surface variance** (0.85 vs 0.73): they
  produce more varied text even repeating the same form — consistent with their role
  as *developing* rather than *rearranging* content.
- Generative forms also produce **more committed verdicts**: socratic_dialogue and
  red_blue_debate both give 5/5 "support" on minimum_wage, where rearrangement forms
  hedged.

### The Hegelian triad specifically (H1a)
`dialectical_triad` is the only form that, on `minimum_wage`, returns **"qualified"
5/5** — i.e., it reliably *refuses the binary* and produces a calibrated synthesis
(inflation-indexed, region-adjusted, with safeguards). This is precisely the Hegelian
prediction: the triad form does not select one of the given poles but produces a
*new, higher determination* (Aufhebung) that was not the raw yes/no. Form did not
rearrange the content; it produced a different *kind* of content.

## Interpretation: does form govern content in an LLM? — **Yes, at the content level.**
- The surface (TF-IDF) measure gives only a weak signal (ratio 1.19) because a
  reasoning model's surface realizations are noisy even within a fixed form, which
  inflates the within-form denominator.
- The **style-stripped verdict measure** shows that, for the same neutral facts and
  the same question, the model's *answer* changes with the form ~28% of the time
  overall, and ~43% on the most genuinely-contested item (minimum_wage).
- The *type* of form matters in a Hegelian way: the dialectical triad systematically
  generates a third, synthetic verdict where others pick a pole; the adversarial
  form defaults to the conservative verdict; the rigid JSON form uniquely nudges
  toward the negative. Each form has a *characteristic content*, not just a
  characteristic style.

**Bottom line:** You cannot hold content fixed and "just" change the format. The
format is already a determination of the result. Hegel's thesis is reproduced — not
as a stylistic effect but as a substantive one — inside an LLM.

## Caveats / next steps
- **n=3 items × 5 repeats** is a pilot. Extend items and repeats for power.
- Verdict classification is a per-item keyword heuristic. An **LLM-judge** extraction
  step (classify the conclusion's stance with the model itself) would remove the
  heuristic and enable arbitrary items.
- TF-IDF is style-leaky; replace with a sentence-embedding model or the LLM-judge for
  a tighter content-vs-style separation.
- `seed` reproducibility held across the run but reasoning-model nondeterminism at
  the surface layer is real; the verdict measure is robust to it by design.
- The minimum_wage result is the strongest single piece of evidence and deserves a
  dedicated replication with more items of genuinely-balanced evidence.

## Reproduce
```
./run.sh experiments   # runs 120 calls → data/raw_runs.jsonl
./run.sh analyze      # → data/analysis.json
```
Config in `runner/config.json`; secrets + venv path in `.env`.