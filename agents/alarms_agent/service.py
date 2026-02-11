import boto3
import time
from datetime import datetime, timedelta

from core.exceptions import AgentExecutionError
from core.ai_runtime import invoke_bedrock
from .prompt_builder import build_alarm_prompt


def fetch_alarms(region: str, alarm_names: list, history_days: int) -> dict:
    """
    Fetch raw alarm state and history from CloudWatch.
    """

    try:
        cw = boto3.client("cloudwatch", region_name=region)

        alarms_response = cw.describe_alarms(
            AlarmNames=alarm_names
        )

        alarms = alarms_response.get("MetricAlarms", [])

        if not alarms:
            return {"alarms": []}

        start_time = datetime.utcnow() - timedelta(days=history_days)

        result = []

        for alarm in alarms:
            history_response = cw.describe_alarm_history(
                AlarmName=alarm["AlarmName"],
                StartDate=start_time,
                HistoryItemType="StateUpdate",
                MaxRecords=20,
                ScanBy="TimestampDescending"
            )

            history_items = history_response.get("AlarmHistoryItems", [])

            structured_history = [
                {
                    "timestamp": item.get("Timestamp").isoformat(),
                    "summary": item.get("HistorySummary"),
                }
                for item in history_items
                if item.get("Timestamp") is not None
            ]

            result.append({
                "alarm_name": alarm.get("AlarmName"),
                "state": alarm.get("StateValue"),
                "metric_name": alarm.get("MetricName"),
                "namespace": alarm.get("Namespace"),
                "recent_history": structured_history
            })

        return {"alarms": result}

    except Exception as e:
        raise AgentExecutionError(f"Failed to fetch alarms: {str(e)}")


def analyze_alarms(alarm_data: dict, model_id: str) -> dict:
    """
    Send alarm data to Bedrock for AI-based pattern detection.
    """

    try:
        start_time = time.time()

        prompt = build_alarm_prompt(alarm_data)

        ai_start = time.time()

        ai_response = invoke_bedrock(
            model_id=model_id,
            prompt=prompt
        )

        ai_latency = round(time.time() - ai_start, 3)
        total_latency = round(time.time() - start_time, 3)

        return {
            "ai_summary": ai_response,
            "metadata": {
                "retry_count": 0,
                "bedrock_latency_seconds": ai_latency,
                "total_latency_seconds": total_latency,
                "prompt_truncated": False
            }
        }

    except Exception as e:
        raise AgentExecutionError(f"Alarm AI analysis failed: {str(e)}")
