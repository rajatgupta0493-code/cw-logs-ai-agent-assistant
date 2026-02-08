import boto3
from typing import Dict, Any


def get_logs_client(region: str):
    return boto3.client("logs", region_name=region)


def start_logs_query(
    client,
    log_groups: list[str],
    query: str,
    start_time: int,
    end_time: int,
) -> Dict[str, Any]:
    return client.start_query(
        logGroupNames=log_groups,
        startTime=start_time,
        endTime=end_time,
        queryString=query,
    )


def get_query_results(client, query_id: str) -> Dict[str, Any]:
    return client.get_query_results(queryId=query_id)
