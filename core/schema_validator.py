REQUIRED_KEYS = [
    "summary",
    "total_records_analyzed",
    "key_patterns",
    "error_signals",
    "observations",
    "insufficient_data",
]


def validate_summary_schema(response_json: dict):
    for key in REQUIRED_KEYS:
        if key not in response_json:
            raise ValueError(f"Missing required key in AI response: {key}")
