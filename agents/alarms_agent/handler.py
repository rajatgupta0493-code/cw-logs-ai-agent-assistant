from core.response_builder import build_success_response, build_error_response
from core.exceptions import ValidationError, AgentExecutionError
from .models import validate_request
from .service import fetch_alarms


def handler(event, context):
    try:
        validated = validate_request(event)

        data = fetch_alarms(
            region=validated["region"],
            alarm_names=validated["alarm_names"],
            history_days=validated["history_days"]
        )

        return build_success_response(data)

    except ValidationError as ve:
        return build_error_response("ValidationError", str(ve))

    except AgentExecutionError as ae:
        return build_error_response("AgentExecutionError", str(ae))

    except Exception as e:
        return build_error_response("UnhandledError", str(e))
