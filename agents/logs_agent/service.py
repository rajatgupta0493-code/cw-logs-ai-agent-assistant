import time
import json
from typing import Any, Dict

from agents.logs_agent.exceptions import AgentExecutionError
from agents.logs_agent.cloudwatch_client import (
    get_logs_client,
    start_logs_query,
    get_query_results,
)
from agents.logs_agent.config_loader import load_config
from agents.logs_agent.prompt_builder import build_prompt

from core.ai_runtime import invoke_bedrock
from core.schema_validator import validate_summary_schema


MAX_WAIT_SECONDS = 600  # 10 minutes
POLL_INTERVAL_SECONDS = 3
MAX_AI_RETRIES = 1


def execute(request: Dict[str, Any]) -> Dict[str, Any]:
    try:
        config = load_config()
        client = get_logs_client(request["region"])

        start_time_total = time.time()

        # 1️⃣ Start Logs Insights Query
        start_response = start_logs_query(
            client=client,
            log_groups=request["log_groups"],
            query=request["query"],
            start_time=request["start_time"],
            end_time=request["end_time"],
        )

        query_id = start_response.get("queryId")

        # 2️⃣ Poll for Completion
        elapsed = 0
        query_completion_time = None

        while elapsed < MAX_WAIT_SECONDS:
            response = get_query_results(client, query_id)
            status = response.get("status")

            if status == "Complete":
                query_completion_time = time.time()
                break

            if status in ["Failed", "Cancelled", "Timeout"]:
                raise AgentExecutionError(
                    f"Query ended with status: {status}"
                )

            time.sleep(POLL_INTERVAL_SECONDS)
            elapsed += POLL_INTERVAL_SECONDS

        if query_completion_time is None:
            raise AgentExecutionError(
                "Query did not complete within 10 minutes."
            )

        # 3️⃣ Prepare Results for LLM
        results = response.get("results", [])
        limited_results = results[: config["max_records_for_summary"]]

        prompt, prompt_truncated = build_prompt(limited_results)

        # 4️⃣ Invoke Bedrock (with retry)
        retry_count = 0
        bedrock_latency = 0

        while retry_count <= MAX_AI_RETRIES:
            try:
                ai_response, bedrock_latency = invoke_bedrock(
                    model_id=config["inference_profile_id"],
                    prompt=prompt,
                )

                validate_summary_schema(ai_response)
                break

            except Exception:
                retry_count += 1
                if retry_count > MAX_AI_RETRIES:
                    raise

        # 5️⃣ Latency Breakdown
        query_latency = round(
            query_completion_time - start_time_total, 3
        )

        total_latency = round(
            time.time() - start_time_total, 3
        )

        # 6️⃣ Structured Logging
        log_payload = {
            "query_id": query_id,
            "retry_count": retry_count,
            "query_latency_seconds": query_latency,
            "bedrock_latency_seconds": bedrock_latency,
            "total_latency_seconds": total_latency,
            "prompt_truncated": prompt_truncated,
        }

        print(json.dumps(log_payload))

        # 7️⃣ Return Response
        return {
            "query_id": query_id,
            "ai_summary": ai_response,
            "metadata": {
                "retry_count": retry_count,
                "query_latency_seconds": query_latency,
                "bedrock_latency_seconds": bedrock_latency,
                "total_latency_seconds": total_latency,
                "prompt_truncated": prompt_truncated,
            },
        }

    except Exception as exc:
        raise AgentExecutionError(str(exc)) from exc
