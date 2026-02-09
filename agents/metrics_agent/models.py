from agents.metrics_agent.exceptions import ValidationError


def validate_request(event: dict):
    required_fields = ["region", "metric_queries", "start_time", "end_time"]

    for field in required_fields:
        if field not in event:
            raise ValidationError(f"Missing required field: {field}")

    if not isinstance(event["metric_queries"], list):
        raise ValidationError("metric_queries must be a list")
