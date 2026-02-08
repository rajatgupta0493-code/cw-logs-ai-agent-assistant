# CW Logs AI Agent Assistant

Open-source, production-safe AI agents for Amazon CloudWatch.

Built using:

- AWS Lambda (Python 3.11)
- AWS CDK (Python)
- Amazon Bedrock (Claude Opus 4.6)
- Direct CLI / SDK invocation
- Stateless architecture

---

# ✅ Current Status (Phase 1 – Logs Agent)

The CloudWatch Logs Insights Agent is fully functional end-to-end.

### What It Does

1. Validates input request
2. Calls `StartQuery`
3. Polls `GetQueryResults` (max 10 minutes)
4. Limits records (configurable)
5. Invokes Claude Opus 4.6 via Bedrock
6. Enforces strict JSON output schema
7. Returns structured AI summary

---

# 🏗 Architecture

```
Lambda
  ↓
Input Validation
  ↓
StartQuery
  ↓
Poll GetQueryResults
  ↓
Limit Results (configurable)
  ↓
Build Prompt
  ↓
Invoke Bedrock (Inference Profile)
  ↓
Strict JSON Extraction
  ↓
Schema Validation
  ↓
Structured AI Response
```

---

# 📦 Output Contract

Every response follows:

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

# 🤖 AI Summary Schema (Strict)

Claude MUST return:

```json
{
  "summary": "string",
  "total_records_analyzed": number,
  "key_patterns": [],
  "error_signals": [],
  "observations": [],
  "insufficient_data": false
}
```

Extra fields are rejected.

Hallucinations are controlled by:

- Strict prompt instructions
- Low temperature (0.1)
- Schema validation
- JSON extraction hardening

---

# ⚙️ Configuration

File:

```
agents/logs_agent/config/logs_agent_config.json
```

Example:

```json
{
  "agent_name": "logs_insights_agent",
  "inference_profile_id": "us.anthropic.claude-opus-4-6-v1",
  "max_query_timeout_seconds": 600,
  "max_records_for_summary": 500
}
```

You can modify:

- Inference profile
- Record limit
- Query timeout

No application logic changes required.

---

# 🚀 Deployment

## Prerequisites

- Python 3.11
- Node.js
- AWS CLI configured
- AWS CDK installed

Install CDK:

```bash
npm install -g aws-cdk
```

---

## Setup Virtual Environment

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Bootstrap (First Time Only)

```bash
cdk bootstrap
```

---

## Deploy

```bash
cdk deploy
```

Confirm with `y`.

---

# 🧪 Invocation Example

```bash
START_TIME=$(($(date +%s) - 3600))
END_TIME=$(date +%s)

aws lambda invoke \
  --function-name <FUNCTION_NAME> \
  --cli-binary-format raw-in-base64-out \
  --payload "{
    \"region\":\"us-east-1\",
    \"log_groups\":[\"cw-agent-test-group\"],
    \"query\":\"fields @message | sort @timestamp desc\",
    \"start_time\":$START_TIME,
    \"end_time\":$END_TIME
  }" \
  response.json
```

View output:

```bash
cat response.json
```

---

# 🔐 IAM Permissions Used

- logs:StartQuery
- logs:GetQueryResults
- bedrock:InvokeModel

Currently scoped to `*` (will be tightened later).

---

# ⏱ Time Constraints

- Lambda timeout: 15 minutes
- Query polling max: 10 minutes
- Poll interval: 3 seconds

---

# 🛡 Safety & Guardrails

- Strict JSON-only AI responses
- Markdown stripping + JSON extraction
- Schema validation
- Deterministic response contract
- Record limit before sending to LLM

---

# 📈 Roadmap

Next:

- Retry-on-invalid JSON
- Prompt token size guardrail
- Structured logging
- Metrics Agent
- Alarms Agent
- Multi-agent modularization

---

# 🔓 Open Source Goals

- Fully configurable
- Replace queries without code changes
- Replace inference profile without code changes
- Minimal dependencies
- Production-safe invocation patterns
