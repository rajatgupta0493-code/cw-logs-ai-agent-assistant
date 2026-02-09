import json
from core.prompt_guardrails import apply_prompt_guardrail


def build_prompt(results: list) -> tuple[str, bool]:
    base_prompt = f"""
You are a CloudWatch Logs Insights summarization engine.

Use ONLY the provided data.
Do NOT invent metrics.
Do NOT speculate.
If data is insufficient, set insufficient_data=true.

Return STRICT JSON with this schema:

{{
  "summary": "string",
  "total_records_analyzed": number,
  "key_patterns": [],
  "error_signals": [],
  "observations": [],
  "insufficient_data": false
}}

CloudWatch Results:
{json.dumps(results, indent=2)}
"""

    return apply_prompt_guardrail(base_prompt)
