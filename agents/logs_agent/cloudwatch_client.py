import boto3
from typing import Dict, Any


def start_logs_query(
    region: str,
    log_groups: list[str],
    query: str,
    start_time: int,
    end_time: int,
) -> Dict[str, Any]:
    client = boto3.client("logs", region_name=region)

    response = client.start_query(
        logGroupNames=log_groups,
        startTime=start_time,
        endTime=end_time,
        queryString=query,
    )

    return response
