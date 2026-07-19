"""Load all form templates from the forms/ directory as {name: FORM_string}."""
from pathlib import Path

_FORMS_DIR = Path(__file__).resolve().parent.parent / "forms"


def load_forms() -> dict:
    forms = {}
    for p in sorted(_FORMS_DIR.glob("*.py")):
        if p.name.startswith("_"):
            continue
        ns = {}
        exec(compile(p.read_text(), str(p), "exec"), ns)
        if "FORM" in ns:
            forms[p.stem] = ns["FORM"]
    return forms


# Form families, used by the analyzer to compare rearrangement vs generative.
REARRANGEMENT = {"bullet_list", "numbered_steps", "json_schema", "qa_pairs", "syllogism"}
GENERATIVE = {"dialectical_triad", "socratic_dialogue", "red_blue_debate"}


def family(form_name: str) -> str:
    if form_name in REARRANGEMENT:
        return "rearrangement"
    if form_name in GENERATIVE:
        return "generative"
    return "other"