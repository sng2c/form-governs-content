# Form Governs Content — An Empirical Test of Hegel in LLMs

> *"Die Form regiert den Inhalt." — Form governs content.* (Hegel)

A pilot study that tests, empirically, whether Hegel's thesis holds *inside* a Large
Language Model: when the **same neutral facts and the same question** are given but
clothed in **different forms**, does the model's output change not merely in style but
in *substantive content* — its verdicts and conclusions?

📖 **Detailed report**: [`report/REPORT.md`](report/REPORT.md) (English) · [`report/REPORT.ko.md`](report/REPORT.ko.md) (한국어)
📑 **Per-item notes**: [`report/ITEMS.md`](report/ITEMS.md) (English) · [`report/ITEMS.ko.md`](report/ITEMS.ko.md) (한국어)
🌐 **한국어 README**: [`README.md`](README.md)
🧪 **MVP multi-model study**: [`report/MVP_STUDY.md`](report/MVP_STUDY.md) (English) · [`report/MVP_STUDY.ko.md`](report/MVP_STUDY.ko.md) (한국어)
🔍 **Exp 3 local triad verification**: [`report/EXP3_STUDY.md`](report/EXP3_STUDY.md) (English) · [`report/EXP3_STUDY.ko.md`](report/EXP3_STUDY.ko.md) (한국어)

---

## 1. Hypotheses

| # | Hypothesis |
|---|---|
| **H1** (Hegel, strong) | Form is not an inert container; it determines what the content *becomes*. Holding raw content, model, seed and temperature fixed while varying only the form makes the *extracted conclusion* diverge more across forms than within a single form repeated. |
| **H1a** (Hegel, dialectical) | Generative forms that force content to *develop through contradiction* (dialectical triad, Socratic dialogue, red/blue debate) produce more novel propositions and more committed/divergent conclusions than rearrangement forms (bullets, JSON, syllogism). In particular the **thesis–antithesis–synthesis triad** refuses the binary and produces a *third, synthetic verdict*. |
| **H0** (style-only) | Form changes only surface style; extracted conclusions converge regardless of form. (Hegel is false for LLMs.) |

## 2. Method (the proof procedure)

### Design — one axis fixed, one varied
| Axis | Held fixed | Varied |
|---|---|---|
| Raw content (neutral facts + contested question) | ✓ (3 items) | |
| Prompt form | | ✓ (8 templates, 2 families) |
| Model, seed, temperature, repetition | ✓ (gpt-oss:120b, T=0.3, seed 42–46, 5 repeats) | |

- **3 controlled items**: `battery_limits` (tech policy), `minimum_wage` (economics),
  `pluto_planet` (science classification). Each is built from facts supporting both sides
  so that form has room to determine the verdict. *Per-item detail: [`report/ITEMS.md`](report/ITEMS.md).*
- **8 forms, 2 families**:
  - Rearrangement (5): `bullet_list`, `numbered_steps`, `json_schema`, `qa_pairs`, `syllogism`.
  - Generative (3): `dialectical_triad` (thesis–antithesis–synthesis), `socratic_dialogue`, `red_blue_debate`.
- **24 cells × 5 repeats = 120 calls** to `gpt-oss:120b` via Ollama Cloud.
- Each output's conclusion is extracted and style-stripped to a single sentence, then
  measured two ways.

### Two measurements — separating a genuine content effect from cosmetics
The key move is to compare only the *conclusion (verdict)*, so a real content effect is
separable from a cosmetic style effect.

1. **TF-IDF surface ratio** = across-form cosine distance ÷ within-form cosine distance.
   `≫1` ⇒ form governs content (H1); `≈1` ⇒ form is cosmetic (H0).
2. **Verdict divergence (style-stripped)**: each conclusion is classified into a per-item
   stance label (`support`/`oppose`/`qualified`…); divergence = `1 − max label share`.
   High divergence ⇒ form determines the *verdict* for the same content ⇒ form governs
   content.

## 3. Conclusion

### Headline numbers (`data/analysis.json`)
| Metric | Value | Reading |
|---|---|---|
| TF-IDF surface ratio (across/within) | **1.19** | >1 (form has an effect) but below the strict 1.5 bar. Reasoning-model surface noise inflates the within-form denominator, under-detecting. |
| within-form variance (rearrangement / generative) | 0.73 / 0.85 | generative forms vary more in surface text even when repeated — the character of *developing* forms. |
| **Verdict divergence (style-stripped), overall** | **0.283** | how often the verdict splits when only the form changes, for the same content. |
| `hegel_h1_verdict` (divergence > 0.15) | **true** | **H1 holds at the content (verdict) level.** |

### Strongest signal: minimum_wage (verdict divergence 0.425)
Same neutral facts, only the form changed, and the **verdict splits**:
- `socratic_dialogue` / `red_blue_debate` → **"support"** 5/5 (clean affirmative)
- `bullet_list` / `syllogism` / `dialectical_triad` → **"qualified"** (hedged/conditional)
- `json_schema` → **drifts toward "oppose"** (the only form split toward the negative)

### The Hegelian triad's exact prediction (H1a)
On `minimum_wage`, `dialectical_triad` returns **"qualified" 5/5** — it consistently
*refuses the binary* and produces a calibrated synthesis (inflation-indexed,
region-adjusted, with safeguards). This is the Hegelian prediction verbatim: the triad
does not rearrange the content but produces a *different kind* of content — an
Aufhebung that was neither raw pole.

### Form-family "characteristic content"
- **Dialogic/adversarial generative forms** commit to more decisive verdicts.
- **Structured/analytical rearrangement forms** hedge to "qualified".
- **Rigid JSON-schema form** uniquely nudges toward the negative.
- On `pluto_planet`, `red_blue_debate` alone leans "keep dwarf planet" (the
  judge-form's conservative default).

### Conclusion
**With the same facts and the same question, changing only the form changes the
model's answer — not its phrasing but its verdict.** The surface (TF-IDF) measure is
weak (~1.19) because a reasoning model's surface realizations are noisy even within a
fixed form, but the style-stripped verdict measure shows divergence ~28% overall
(~43% on the most genuinely-contested item). **Format is not engineering polish — it is
part of the determination of the result.** Hegel's thesis is reproduced inside an LLM
*substantively*, not stylistically.

> Caveats: n=3 items × 5 repeats (pilot) · verdict classification is a per-item keyword
> heuristic · TF-IDF is style-leaky. Natural next steps: LLM-judge verdict extraction and
> sentence-embedding. See the detailed report for full caveats and extensions.

## Repository layout
```
form-governs-content/
├── README.md               this overview (한국어)
├── README.en.md            English overview (this file)
├── run.sh                  loads .env + activates venv + runs pipeline
├── requirements.txt
├── .env                    OLLAMA_API_KEY + VENV_ACTIVATE (gitignored)
├── forms/                  8 form templates (with philosophical notes)
├── content/dataset.json    3 controlled content items (facts + contested question)
├── runner/                 config.json / forms.py / llm.py / run_experiments.py
├── analyze/                extract.py (conclusion) / analyze.py (metrics)
├── report/
│   ├── REPORT.md           detailed report (English)
│   ├── REPORT.ko.md        detailed report (한국어)
│   ├── ITEMS.md            per-item notes (English)
│   └── ITEMS.ko.md         per-item notes (한국어)
└── data/                   raw_runs.jsonl + analysis.json (gitignored)
```

## Reproduce
```bash
cp .env.example .env   # fill OLLAMA_API_KEY and VENV_ACTIVATE
./run.sh experiments   # 120 calls → data/raw_runs.jsonl
./run.sh analyze       # → data/analysis.json
```
Config: `runner/config.json` (model, temperature, seed, repeats, forms). Deps:
`python-dotenv`, `requests`, `numpy`, `scikit-learn`.