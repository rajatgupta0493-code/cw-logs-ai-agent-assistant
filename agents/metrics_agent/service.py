import json
from typing import Dict, Any

from agents.metrics_agent.exceptions import AgentExecutionError
from agents.metrics_agent.cloudwatch_client import (
    get_metrics_client,
    get_metric_data,
)
from agents.metrics_agent.models import validate_request


def execute(event: Dict[str, Any]) -> Dict[str, Any]:
    try:
        validate_request(event)

        client = get_metrics_client(event["region"])

        response = get_metric_data(
            client=client,
            metric_queries=event["metric_queries"],
            start_time=event["start_time"],
            end_time=event["end_time"],
        )

        return {
            "status": "success",
            "data": {
                "metrics": response.get("MetricDataResults", [])
            },
            "error": None,
        }

    except Exception as exc:
        raise AgentExecutionError(str(exc)) from exc
