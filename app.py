#!/usr/bin/env python3
import aws_cdk as cdk
from infrastructure.logs_agent_stack import LogsAgentStack

app = cdk.App()
LogsAgentStack(app, "LogsAgentStack")

app.synth()
