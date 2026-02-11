from core.response_builder import build_success_response, build_error_response
from core.exceptions import ValidationError, AgentExecutionError
from .models import validate_request
from .service import analyze_alarms, fetch_alarms
from agents.logs_agent.config_loader import load_config


def handler(event, context):
    try:
        validated = validate_request(event)

        raw_alarm_data = fetch_alarms(
            region=validated["region"],
            alarm_names=validated["alarm_names"],
            history_days=validated["history_days"]
        )

        config = load_config()
        model_id = config["inference_profile_id"]

        ai_result = analyze_alarms(
            alarm_data=raw_alarm_data,
            model_id=model_id
        )

        return build_success_response(ai_result)

    except ValidationError as ve:
        return build_error_response("ValidationError", str(ve))

    except AgentExecutionError as ae:
        return build_error_response("AgentExecutionError", str(ae))

    except Exception as e:
        return build_error_response("UnhandledError", str(e))
