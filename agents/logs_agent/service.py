from typing import Any, Dict

from exceptions import AgentExecutionError
from cloudwatch_client import start_logs_query


def execute(request: Dict[str, Any]) -> Dict[str, Any]:
    try:
        response = start_logs_query(
            region=request["region"],
            log_groups=request["log_groups"],
            query=request["query"],
            start_time=request["start_time"],
            end_time=request["end_time"],
        )

        return {
            "message": "Query started successfully.",
            "query_id": response.get("queryId"),
        }

    except Exception as exc:
        raise AgentExecutionError(str(exc)) from exc
