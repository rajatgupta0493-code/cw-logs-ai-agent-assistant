import time
from typing import Any, Dict

from exceptions import AgentExecutionError
from cloudwatch_client import (
    get_logs_client,
    start_logs_query,
    get_query_results,
)


MAX_WAIT_SECONDS = 600  # 10 minutes
POLL_INTERVAL_SECONDS = 3


def execute(request: Dict[str, Any]) -> Dict[str, Any]:
    try:
        client = get_logs_client(request["region"])

        start_response = start_logs_query(
            client=client,
            log_groups=request["log_groups"],
            query=request["query"],
            start_time=request["start_time"],
            end_time=request["end_time"],
        )

        query_id = start_response.get("queryId")

        elapsed = 0

        while elapsed < MAX_WAIT_SECONDS:
            response = get_query_results(client, query_id)
            status = response.get("status")

            if status == "Complete":
                return {
                    "query_id": query_id,
                    "results": response.get("results", []),
                    "statistics": response.get("statistics", {}),
                }

            if status in ["Failed", "Cancelled", "Timeout"]:
                raise AgentExecutionError(
                    f"Query ended with status: {status}"
                )

            time.sleep(POLL_INTERVAL_SECONDS)
            elapsed += POLL_INTERVAL_SECONDS

        raise AgentExecutionError(
            "Query did not complete within 10 minutes."
        )

    except Exception as exc:
        raise AgentExecutionError(str(exc)) from exc
