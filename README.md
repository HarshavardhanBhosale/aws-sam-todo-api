# Serverless TODO API on AWS (Beginner Project)

A beginner-friendly **serverless REST API** using **AWS Lambda + API Gateway (HTTP API) + DynamoDB**, deployed with **AWS SAM**.  
Ideal to showcase on GitHub with clear, reproducible steps and **zero cost when deleted**.

## What you’ll build
- `POST /todos` – create a todo
- `GET /todos/{id}` – get a todo by id
- `GET /todos` – list all todos
- `DELETE /todos/{id}` – delete a todo
- Data stored in DynamoDB. One Lambda handles all routes to stay simple.

## Architecture
Client → API Gateway (HTTP API) → Lambda (Python) → DynamoDB

## Prerequisites
- AWS account + an IAM user with programmatic access
- **AWS CLI** installed and configured (`aws configure`, set region e.g. `ap-south-1`)
- **SAM CLI** installed (https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
- Optional: Docker (for `sam local` testing)

## Quickstart

```bash
# 1) Clone this repo and enter it
git clone <your-repo-url>.git aws-sam-todo-api
cd aws-sam-todo-api

# 2) (Optional) create virtualenv and install deps
python -m venv .venv && source .venv/bin/activate  # PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 3) Build & deploy with SAM
sam build
sam deploy --guided
# Answer prompts: Stack name (e.g., todo-api), Region (e.g., ap-south-1), Confirm changeset: Y, Allow SAM to create roles: Y, Save arguments: Y

# 4) Get your endpoint from the output (ApiEndpoint). Example:
# https://abc123.execute-api.ap-south-1.amazonaws.com
```

## Test the API

```bash
API="https://<your-api-id>.execute-api.<region>.amazonaws.com"

# Create
curl -X POST "$API/todos" -d '{"title":"learn aws","done":false}' -H "Content-Type: application/json"

# List
curl "$API/todos"

# Get by id
curl "$API/todos/<id-from-create-response>"

# Delete
curl -X DELETE "$API/todos/<id-from-create-response>"
```

## Local testing (optional)

```bash
sam local start-api
# Then call http://127.0.0.1:3000/todos etc.
```

## Cleanup (avoid charges)
```bash
sam delete
# Confirms and removes: API Gateway, Lambda, DynamoDB table, and deployment bucket.
```

## Repo structure
```
aws-sam-todo-api/
├── src/
│   └── app.py
├── events/
│   └── create.json
├── template.yaml
├── requirements.txt
├── .gitignore
└── README.md
```

## Push to GitHub

```bash
# From project root
git init
git add .
git commit -m "feat: serverless TODO API (SAM + Lambda + DynamoDB)"
git branch -M main
git remote add origin https://github.com/<your-username>/aws-sam-todo-api.git
git push -u origin main
```

Add this sentence to your README for recruiters:

> **Note:** The AWS stack is deleted after testing to avoid costs. Recreate it anytime using `sam build && sam deploy`.
