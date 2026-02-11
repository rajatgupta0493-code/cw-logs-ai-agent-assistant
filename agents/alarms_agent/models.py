from typing import List
from core.exceptions import ValidationError


def validate_request(event: dict) -> dict:
    if not isinstance(event, dict):
        raise ValidationError("Request payload must be a JSON object.")

    region = event.get("region")
    alarm_names = event.get("alarm_names")
    history_days = event.get("history_days", 1)

    if not region:
        raise ValidationError("Missing required field: region")

    if not alarm_names or not isinstance(alarm_names, list):
        raise ValidationError("alarm_names must be a non-empty list")

    if not isinstance(history_days, int) or history_days <= 0:
        raise ValidationError("history_days must be a positive integer")

    return {
        "region": region,
        "alarm_names": alarm_names,
        "history_days": history_days,
    }
