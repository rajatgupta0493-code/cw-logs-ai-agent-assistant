import json
import boto3
import re
from botocore.exceptions import ClientError


def extract_json(text: str) -> dict:
    text = re.sub(r"```json|```", "", text).strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return json.loads(match.group())

    raise ValueError("Model did not return valid JSON.")


def invoke_bedrock(model_id: str, prompt: str) -> tuple[dict, float]:
    client = boto3.client("bedrock-runtime")

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "temperature": 0.1,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:
        import time
        start = time.time()

        response = client.invoke_model(
            modelId=model_id,
            body=json.dumps(body),
            contentType="application/json",
            accept="application/json"
        )

        latency = round(time.time() - start, 3)

        response_body = json.loads(response["body"].read())
        text_output = response_body["content"][0]["text"]

        return extract_json(text_output), latency

    except ClientError as e:
        error_code = e.response["Error"]["Code"]

        if error_code == "ThrottlingException":
            raise RuntimeError("BedrockThrottled") from e
        if error_code == "ModelTimeoutException":
            raise RuntimeError("BedrockTimeout") from e
        if error_code == "ServiceUnavailableException":
            raise RuntimeError("BedrockUnavailable") from e

        raise
