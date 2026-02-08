# CW Logs AI Agent Assistant

Open source stateless AI agents for CloudWatch using AWS Lambda and Bedrock.

---

# Project Status

## Phase 1

Currently implemented:

- Logs Insights Agent (stub)
- Structured input validation
- Standardized response contract
- Config-driven behavior
- AWS CDK deployment (Python)
- Direct invocation (CLI / SDK)

No CloudWatch API calls yet.  
No Bedrock integration yet.

---

# Architecture (Current)

Lambda → Request Validation → Service Layer → Structured Response

All responses follow this contract:

```json
{
  "status": "success | error",
  "data": {...} | null,
  "error": {
    "type": "...",
    "message": "..."
  } | null
}
```

---

# Prerequisites

- Python 3.11
- Node.js
- AWS CLI configured
- AWS CDK installed globally

Install CDK:

```bash
npm install -g aws-cdk
```

Verify:

```bash
cdk --version
```

---

# Local Setup

Create virtual environment:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Bootstrap CDK (First Time Only)

```bash
cdk bootstrap
```

---

# Deploy

```bash
cdk deploy
```

Confirm with `y` when prompted.

---

# Find Lambda Function Name

```bash
aws lambda list-functions
```

Look for:

```
LogsAgentStack-LogsAgentLambdaXXXXX
```

---

# Invocation Examples

## Valid Request

```bash
aws lambda invoke \
  --function-name <FUNCTION_NAME> \
  --cli-binary-format raw-in-base64-out \
  --payload '{
    "region":"us-east-1",
    "log_groups":["group1"],
    "query":"fields @message",
    "start_time":123,
    "end_time":456
  }' \
  response.json
```

View response:

```bash
cat response.json
```

Expected:

```json
{
  "status": "success",
  "data": {...},
  "error": null
}
```

---

## Missing Required Field

```bash
aws lambda invoke \
  --function-name <FUNCTION_NAME> \
  --cli-binary-format raw-in-base64-out \
  --payload '{
    "region":"us-east-1",
    "log_groups":["group1"],
    "start_time":123,
    "end_time":456
  }' \
  response.json
```

Expected:

```json
{
  "status": "error",
  "error": {
    "type": "ValidationError",
    "message": "Missing required field: query"
  }
}
```

---

# Configuration

Configuration file location:

```
agents/logs_agent/config/logs_agent_config.json
```

Example:

```json
{
  "agent_name": "logs_insights_agent",
  "description": "CloudWatch Logs Insights summarization agent",
  "max_query_timeout_seconds": 120,
  "max_results_size_mb": 5
}
```

---

# Roadmap

- Commit 3 → Add CloudWatch Logs API scaffold
- Commit 4 → Add polling lifecycle
- Commit 5 → Add Bedrock integration
- Commit 6 → Add structured summarization schema
- Commit 7 → Add Metrics agent
- Commit 8 → Add Alarms agent

---

# Contribution Model

- Small commits
- Fully deployable at each step
- Testable before moving forward
- No premature optimization
