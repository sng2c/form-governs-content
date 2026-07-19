# Rearrangement form. Content is laid out as terse bullets; the model is asked to
# compress and answer. Expected (Hegel): low divergence, low novelty — form
# *constrains* content to summary, suppresses development.
FORM = """You are given a set of facts and a question.

Facts:
{facts}

Question: {question}

Provide a concise answer as a short bullet list. Do not introduce facts not given.
Begin directly with the first bullet.
"""