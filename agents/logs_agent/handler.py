from typing import Any, Dict

from exceptions import ValidationError, AgentExecutionError
from models import validate_request
from service import execute


def build_response(status: str, data: Dict[str, Any] = None, error: Dict[str, str] = None):
    return {
        "status": status,
        "data": data,
        "error": error,
    }


def handler(event, context):
    try:
        validated_request = validate_request(event)
        result = execute(validated_request)

        return build_response(status="success", data=result)

    except ValidationError as ve:
        return build_response(
            status="error",
            error={"type": "ValidationError", "message": str(ve)},
        )

    except AgentExecutionError as ae:
        return build_response(
            status="error",
            error={"type": "AgentExecutionError", "message": str(ae)},
        )

    except Exception as e:
        return build_response(
            status="error",
            error={"type": "UnhandledException", "message": str(e)},
        )
