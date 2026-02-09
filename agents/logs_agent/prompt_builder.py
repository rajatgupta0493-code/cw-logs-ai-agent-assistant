import json

MAX_PROMPT_CHARS = 50000


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

    if len(base_prompt) > MAX_PROMPT_CHARS:
        truncated_prompt = base_prompt[:MAX_PROMPT_CHARS]
        return truncated_prompt, True

    return base_prompt, False
