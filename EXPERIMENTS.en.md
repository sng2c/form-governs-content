# Experiments Index (sequence & result map)

This repo runs **two experiments**, in sequence, testing whether "form governs content"
in LLMs. Use this map to distinguish each experiment's question, design, files (config,
runner, analysis, data, report), reproduce command, and key result.

| # | Experiment | Question | Design | Data | Reports |
|---|---|---|---|---|---|
| **Exp 1** | Does form govern content (single model, 8 forms) | Does changing only the form change the verdict? | 1 model × 8 forms × 3 items × 5 repeats = **120** | `raw_runs.jsonl`·`analysis.json` | `REPORT.*`, `ITEMS.*` |
| **Exp 2** | Pruner MVP multi-model | How does the purpose→template binding vary across model types? | 8 models × 3 purposes × 2 items × 2 repeats = **96** | `mvp_runs.jsonl`·`mvp_analysis.json` | `MVP_STUDY.*` |

**Sequence & dependency:** Exp 1 → (Pruner MVP compromise approved) → Exp 2. Exp 2 reuses
Exp 1's forms/items and validates the Pruner linear spine.

---

## Exp 1 — Does form govern content (single model · 8 forms)

- **Question:** Given the same neutral facts and question, does changing **only the form**
  change the output not in phrasing but in *verdict*?
- **Design:** fixed `gpt-oss:120b`, 8 forms (5 rearrangement + 3 generative), 3 controlled
  items, 5 repeats = **120 completions**. Measures: TF-IDF surface ratio + style-stripped
  verdict divergence.
- **Files:**
  - config: `runner/config.json`
  - runner: `runner/run_experiments.py` → `data/raw_runs.jsonl` (log `data/experiment.log`)
  - analysis: `analyze/analyze.py`, `analyze/extract.py` (conclusion extraction) → `data/analysis.json`
  - reports: `report/REPORT.ko.md` · `report/REPORT.md`, `report/ITEMS.ko.md` · `report/ITEMS.md`
- **Reproduce:**
  ```bash
  source .venv/bin/activate && source .env
  ./run.sh experiments      # = python -m runner.run_experiments
  python -m analyze.analyze
  ```
- **Key result:** TF-IDF ratio 1.19 (effect exists, noise-limited); **style-stripped verdict
  divergence 0.283 → H1 holds at the content (verdict) level**. Strongest split on the most
  contested item (minimum_wage, 0.425). The Hegelian triad refuses the binary and produces
  a third synthesis (H1a).

## Exp 2 — Pruner MVP multi-model (purpose→template binding × 8 model types)

- **Origin:** approved Pruner (MVP) compromise. With $\Phi$ (ideal-template generation)
  kept a black box, the linear spine (purpose→bind→run→human judge) is exercised across
  diverse model types.
- **Question:** How does the purpose→template binding govern the form's *structure* vs
  *verdict* across model types?
- **Design:** 3 purposes (`decide/synthesize/surface_assumptions`) → binding
  (`red_blue_debate/dialectical_triad/socratic_dialogue`) × 2 items × 8 model types × 2
  repeats = **96 completions**.
- **Files:**
  - config: `runner/mvp_config.json`
  - runner: `runner/run_mvp.py` → `data/mvp_runs.jsonl` (log `data/mvp_run.log`)
  - analysis: `analyze/analyze_mvp.py` → `data/mvp_analysis.json`
  - reports: `report/MVP_STUDY.ko.md` · `report/MVP_STUDY.md`
- **Reproduce:**
  ```bash
  source .venv/bin/activate && source .env
  python -m runner.run_mvp
  python -m analyze.analyze_mvp
  ```
- **Key result:** (1) Form's governance of **structure** is model-independent (marker
  realization ~1.0, only general-moe 0.75–0.875). (2) Form's governance of the **verdict**
  is model-dependent — `minimum_wage/decide` splits support/oppose under the same form →
  $\Phi$ staying a black box is justified. (3) **Aufhebung (triad synthesis)** is
  reproduced across all model types (novelty 0.71–0.89, H1a robust).

## Shared infrastructure (both experiments)
- `runner/forms.py` — 8 form templates + family classification
- `runner/llm.py` — Ollama-Cloud (OpenAI-compatible) client (`chat` + metadata `chat_meta`)
- `content/dataset.json` — 3 controlled content items (neutral facts + contested question)
- `forms/` — form templates (with philosophical notes)

## Directory → experiment mapping
```
runner/
  config.json          ── Exp 1 config
  run_experiments.py   ── Exp 1 runner
  mvp_config.json      ── Exp 2 config
  run_mvp.py           ── Exp 2 runner
  forms.py / llm.py    ── shared
analyze/
  extract.py / analyze.py    ── Exp 1 analysis
  analyze_mvp.py             ── Exp 2 analysis
data/ (gitignored; analysis.json & mvp_analysis.json are committed)
  raw_runs.jsonl + analysis.json      ── Exp 1
  mvp_runs.jsonl + mvp_analysis.json  ── Exp 2
report/
  REPORT.* / ITEMS.*        ── Exp 1
  MVP_STUDY.*               ── Exp 2
```