# CW Logs AI Agent Assistant

Open source stateless AI agents for CloudWatch using AWS Lambda and Bedrock.

## Phase 1

Currently implemented:

- Logs Insights Agent (stub)
- Loads configuration
- Returns config on invocation

## Deployment

### 1. Setup

python3.11 -m venv .venv  
source .venv/bin/activate  
pip install -r requirements.txt  

### 2. Bootstrap CDK (first time only)

cdk bootstrap

### 3. Deploy

cdk deploy

## Invocation

aws lambda list-functions

aws lambda invoke \
  --function-name LogsAgentStack-LogsAgentLambdaXXXX \
  --payload '{"test": "hello"}' \
  response.json
