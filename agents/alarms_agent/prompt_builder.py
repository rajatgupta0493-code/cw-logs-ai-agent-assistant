import json


def build_alarm_prompt(alarm_data: dict) -> str:
    return f"""
You are an observability AI assistant.

Analyze the following CloudWatch alarm data.
Detect:
- Flapping alarms (frequent state oscillations)
- Persistent alarms
- Correlated alarm clusters
- Noisy alarms
- Systemic patterns

Rules:
- Use ONLY provided data.
- Do NOT speculate.
- If insufficient history, set insufficient_data=true.
- Output STRICT JSON only.
- Do NOT include explanations outside JSON.

Alarm Data:
{json.dumps(alarm_data, indent=2)}

Return JSON in this exact format:

{{
  "summary": "...",
  "total_alarms_analyzed": 0,
  "current_alarm_states": [],
  "flapping_alarms": [],
  "persistent_alarms": [],
  "correlated_clusters": [],
  "observations": [],
  "insufficient_data": false
}}
"""
