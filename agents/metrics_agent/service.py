import time
import json
from typing import Dict, Any

from agents.metrics_agent.exceptions import AgentExecutionError
from agents.metrics_agent.cloudwatch_client import (
    get_metrics_client,
    get_metric_data,
)
from agents.metrics_agent.models import validate_request
from agents.metrics_agent.config_loader import load_config
from agents.metrics_agent.prompt_builder import build_prompt

from core.ai_runtime import invoke_bedrock
from core.schema_validator import validate_summary_schema


MAX_AI_RETRIES = 1


def execute(event: Dict[str, Any]) -> Dict[str, Any]:
    try:
        validate_request(event)
        config = load_config()

        start_time_total = time.time()

        client = get_metrics_client(event["region"])

        response = get_metric_data(
            client=client,
            metric_queries=event["metric_queries"],
            start_time=event["start_time"],
            end_time=event["end_time"],
        )

        metric_results = response.get("MetricDataResults", [])
        limited_results = metric_results[: config["max_metrics_for_summary"]]

        prompt, prompt_truncated = build_prompt(limited_results)

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

        total_latency = round(time.time() - start_time_total, 3)

        log_payload = {
            "retry_count": retry_count,
            "bedrock_latency_seconds": bedrock_latency,
            "total_latency_seconds": total_latency,
            "prompt_truncated": prompt_truncated,
        }

        print(json.dumps(log_payload))

        return {
            "status": "success",
            "data": {
                "ai_summary": ai_response,
                "metadata": {
                    "retry_count": retry_count,
                    "bedrock_latency_seconds": bedrock_latency,
                    "total_latency_seconds": total_latency,
                    "prompt_truncated": prompt_truncated,
                },
            },
            "error": None,
        }

    except Exception as exc:
        raise AgentExecutionError(str(exc)) from exc
