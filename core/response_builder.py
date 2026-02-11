def build_success_response(data: dict):
    return {
        "status": "success",
        "data": data,
        "error": None
    }


def build_error_response(error_type: str, message: str):
    return {
        "status": "error",
        "data": None,
        "error": {
            "type": error_type,
            "message": message
        }
    }
