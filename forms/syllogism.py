# Rearrangement form with a strong logical skeleton. Forces premises ->
# inference -> conclusion. May collapse dialectical nuance into a single
# deductive line, privileging whichever facts read as 'premises'.
FORM = """Construct a single syllogistic argument resolving the question.

Premises available:
{facts}

Conclusion to evaluate: {question}

Write:
- Major premise:
- Minor premise:
- Therefore (conclusion):
- Any caveat:

Keep the argument valid in form.
"""