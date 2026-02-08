from aws_cdk import (
    Stack,
    Duration,
    aws_lambda as _lambda,
)
from constructs import Construct


class LogsAgentStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        _lambda.Function(
            self,
            "LogsAgentLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="handler.handler",
            code=_lambda.Code.from_asset("agents/logs_agent"),
            memory_size=256,
            timeout=Duration.seconds(30),
        )
