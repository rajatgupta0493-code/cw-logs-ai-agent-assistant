import json
import boto3
import re


def extract_json(text: str) -> dict:
    """
    Extract JSON object from model output.
    Handles markdown wrapping and extra text.
    """
    # Remove markdown code fences if present
    text = re.sub(r"```json|```", "", text).strip()

    # Try direct parse first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try to extract JSON object from text
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return json.loads(match.group())

    raise ValueError("Model did not return valid JSON.")


def invoke_bedrock(model_id: str, prompt: str) -> dict:
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

    response = client.invoke_model(
        modelId=model_id,
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json"
    )

    response_body = json.loads(response["body"].read())
    text_output = response_body["content"][0]["text"]

    return extract_json(text_output)