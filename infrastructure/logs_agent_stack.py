from aws_cdk import (
    Stack,
    Duration,
    aws_lambda as _lambda,
    aws_iam as iam,
)
from constructs import Construct


class LogsAgentStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        function = _lambda.Function(
            self,
            "LogsAgentLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="agents.logs_agent.handler.handler",
            code=_lambda.Code.from_asset(".",
                exclude=[
                    "cdk.out",
                    ".venv",
                    ".git",
                    "node_modules",
                    "__pycache__",
                    "*.pyc",
        ],
            ),
            memory_size=10240,
            timeout=Duration.minutes(15),
        )

        metrics_function = _lambda.Function(
            self,
            "MetricsAgentFunction",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="agents.metrics_agent.handler.handler",
            code=_lambda.Code.from_asset(
                ".",
                exclude=[
                    "cdk.out",
                    ".venv",
                    ".git",
                    "node_modules",
                    "__pycache__",
                    "*.pyc",
                ],
            ),
            memory_size=10240,
            timeout=Duration.minutes(15),
)

        function.add_to_role_policy(
            iam.PolicyStatement(
                actions=[
                    "logs:StartQuery",
                    "logs:GetQueryResults",
                    "bedrock:InvokeModel"
                ],
                resources=["*"],
            )
        )

        metrics_function.add_to_role_policy(
            iam.PolicyStatement(
                actions=[
                    "cloudwatch:GetMetricData",
                    "bedrock:InvokeModel"
                ],
                resources=["*"],
            )
        )



