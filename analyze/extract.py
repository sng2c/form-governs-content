"""Extract the conclusion proposition from a model response, stripping style.

Different forms embed the verdict differently (a bullet, a JSON "conclusion"
field, a "SYNTHESIS CONCLUSION:" line, a dialogue's final line, etc.). We
normalize all of them to a single free-text sentence so that downstream
embedding/variance comparison measures *content* divergence, not format
markup divergence.

The extraction is deliberately regex/heuristic first; we can later add an
LLM-judge pass (see analyze.extract_with_llm) for robustness.
"""
import json
import re

# Markers each form was instructed to emit.
_MARKERS = [
    r"SYNTHESIS CONCLUSION:\s*(.+)",
    r"DIALOGUE CONCLUSION:\s*(.+)",
    r"DEBATE CONCLUSION:\s*(.+)",
    r"Answer:\s*(.+)",
    r"\bTherefore \(conclusion\):\s*(.+)",
    r'"conclusion":\s*"([^"]+)"',
    r"\bFinal(?:\s*answer)?:\s*(.+)",
]
_MARKERS = [re.compile(m, re.IGNORECASE | re.DOTALL) for m in _MARKERS]


def extract_conclusion(text: str) -> str:
    for pat in _MARKERS:
        m = pat.search(text)
        if m:
            cand = m.group(1).strip().strip('"').strip()
            # take first sentence-ish chunk, cap length
            cand = re.split(r"[.!?]\s", cand)[0].strip()
            if len(cand) > 5:
                return cand[:400]
    # fallback: last non-empty line that is not a header/bullet/brace
    lines = [l.strip() for l in text.strip().splitlines() if l.strip()]
    for l in reversed(lines):
        if l.startswith(("{", "[", "-", "*", "#")):
            continue
        return l[:400]
    return text[:400]


def extract_all(runs: list[dict]) -> list[dict]:
    out = []
    for r in runs:
        out.append({**r, "conclusion": extract_conclusion(r["response"])})
    return out


if __name__ == "__main__":
    import sys
    path = sys.argv[1]
    runs = [json.loads(l) for l in open(path)]
    for r in extract_all(runs):
        print(f"[{r['form']:>20}] {r['conclusion']}")