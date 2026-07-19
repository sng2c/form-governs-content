# Rearrangement form. Content is forced into a rigid structured schema.
# Structured output tends to elicit commitment and completeness; may reduce
# hedging and force a determinate verdict where prose would be ambivalent.
FORM = """Respond ONLY with a JSON object matching this schema:

{{
  "facts_given": [string],
  "reasoning": [string],
  "conclusion": string,
  "confidence": "low" | "medium" | "high"
}}

Facts:
{facts}

Question: {question}

Output the JSON and nothing else.
"""