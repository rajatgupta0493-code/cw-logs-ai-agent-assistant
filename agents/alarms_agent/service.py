import boto3
from datetime import datetime, timedelta
from core.exceptions import AgentExecutionError


def fetch_alarms(region: str, alarm_names: list, history_days: int) -> dict:
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
        raise AgentExecutionError(str(e))
