import json
import os
import uuid
from decimal import Decimal

import boto3

dynamodb = boto3.resource("dynamodb")
TABLE_NAME = os.environ.get("TABLE_NAME")
table = dynamodb.Table(TABLE_NAME)


def _resp(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "*",
        },
        "body": json.dumps(body, default=_json_default),
    }


def _json_default(obj):
    if isinstance(obj, Decimal):
        # Convert DynamoDB Decimals to native floats/ints
        if obj % 1 == 0:
            return int(obj)
        return float(obj)
    raise TypeError


def lambda_handler(event, context):
    method = event.get("requestContext", {}).get("http", {}).get("method")
    raw_path = event.get("rawPath", "/")
    path_params = event.get("pathParameters") or {}
    body = event.get("body")

    try:
        if raw_path.startswith("/todos"):
            if method == "GET":
                if "id" in path_params and path_params["id"]:
                    return get_todo(path_params["id"])
                else:
                    return list_todos()
            elif method == "POST":
                return create_todo(body)
            elif method == "DELETE":
                if "id" not in path_params or not path_params["id"]:
                    return _resp(400, {"message": "Missing id in path"})
                return delete_todo(path_params["id"])

        return _resp(404, {"message": "Not found"})
    except Exception as e:
        # Log e in real projects
        return _resp(500, {"message": "Server error", "error": str(e)})


def create_todo(body):
    if not body:
        return _resp(400, {"message": "Missing request body"})
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return _resp(400, {"message": "Invalid JSON"})

    title = data.get("title")
    done = bool(data.get("done", False))

    if not title:
        return _resp(400, {"message": "Field 'title' is required"})

    item = {
        "id": str(uuid.uuid4()),
        "title": title,
        "done": done,
    }
    table.put_item(Item=item)
    return _resp(201, item)


def get_todo(todo_id: str):
    res = table.get_item(Key={"id": todo_id})
    item = res.get("Item")
    if not item:
        return _resp(404, {"message": "Todo not found"})
    return _resp(200, item)


def list_todos():
    res = table.scan()
    items = res.get("Items", [])
    return _resp(200, items)


def delete_todo(todo_id: str):
    # Check existence first (optional)
    res = table.get_item(Key={"id": todo_id})
    if "Item" not in res:
        return _resp(404, {"message": "Todo not found"})
    table.delete_item(Key={"id": todo_id})
    return _resp(200, {"message": "Deleted", "id": todo_id})
