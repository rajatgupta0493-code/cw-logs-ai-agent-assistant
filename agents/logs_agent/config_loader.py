import json
from pathlib import Path


CONFIG_PATH = Path(__file__).parent / "config" / "logs_agent_config.json"


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Config file not found at {CONFIG_PATH}")

    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        return json.load(file)
