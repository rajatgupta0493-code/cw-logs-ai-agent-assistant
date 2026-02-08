from config_loader import load_config


def handler(event, context):
    config = load_config()

    return {
        "status": "ok",
        "agent": config.get("agent_name"),
        "config": config,
        "input_event": event,
    }
