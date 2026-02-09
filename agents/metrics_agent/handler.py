from agents.metrics_agent.service import execute
from agents.metrics_agent.exceptions import (
    ValidationError,
    AgentExecutionError,
)


def handler(event, context):
    try:
        return execute(event)

    except ValidationError as ve:
        return {
            "status": "error",
            "data": None,
            "error": {
                "type": "ValidationError",
                "message": str(ve),
            },
        }

    except AgentExecutionError as ae:
        return {
            "status": "error",
            "data": None,
            "error": {
                "type": "AgentExecutionError",
                "message": str(ae),
            },
        }
