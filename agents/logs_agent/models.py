from typing import Any, Dict, List

from agents.logs_agent.exceptions import ValidationError

REQUIRED_FIELDS = ["region", "log_groups", "query", "start_time", "end_time"]


def validate_request(event: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(event, dict):
        raise ValidationError("Event must be a JSON object.")

    for field in REQUIRED_FIELDS:
        if field not in event:
            raise ValidationError(f"Missing required field: {field}")

    if not isinstance(event["log_groups"], list):
        raise ValidationError("log_groups must be a list.")

    if not isinstance(event["region"], str):
        raise ValidationError("region must be a string.")

    return event
