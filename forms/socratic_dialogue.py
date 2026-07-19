# GENERATIVE form. A dialogue that elicits, tests, and revises claims through
# questioning. Develops content dynamically; tends to surface the strongest
# counter-position to each claim, similar in spirit to determinate negation.
FORM = """Resolve the question as a short Socratic dialogue between two speakers, "Q" and "A".

Facts both speakers share:
{facts}

Question to resolve: {question}

The dialogue must:
- have Q probe A's claims at least 3 times,
- have A revise at least once under pressure,
- end with A stating a final, possibly changed, position.

Conclude with a line: "DIALOGUE CONCLUSION: <one sentence>."
"""