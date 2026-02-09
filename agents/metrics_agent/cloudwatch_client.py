import boto3


def get_metrics_client(region: str):
    return boto3.client("cloudwatch", region_name=region)


def get_metric_data(
    client,
    metric_queries: list,
    start_time: int,
    end_time: int,
):
    formatted_queries = []

    for mq in metric_queries:
        formatted_queries.append(
            {
                "Id": mq["id"],
                "MetricStat": {
                    "Metric": {
                        "Namespace": mq["namespace"],
                        "MetricName": mq["metric_name"],
                        "Dimensions": mq["dimensions"],
                    },
                    "Period": mq["period"],
                    "Stat": mq["stat"],
                },
                "ReturnData": True,
            }
        )

    response = client.get_metric_data(
        MetricDataQueries=formatted_queries,
        StartTime=start_time,
        EndTime=end_time,
    )

    return response
