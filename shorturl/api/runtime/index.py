import json
import boto3  # type: ignore
import os
import random
import string

from functools import lru_cache


client = boto3.client("dynamodb")


@lru_cache(maxsize=10)
def read_short_url(raw_path):
    data = client.get_item(
        TableName=os.getenv("DYNAMODB_TABLE_NAME"),
        Key={"ShortURL": {"S": raw_path}},
    )
    if "Item" in data:
        return data["Item"]["FullURL"]["S"]
    else:
        return None


@lru_cache(maxsize=10000)
def write_short_url(long_url):
    # Create ShortURL
    short_url = "".join(random.choices(string.ascii_letters, k=4))
    # Save to DynamoDB
    client.put_item(
        TableName=os.getenv("DYNAMODB_TABLE_NAME"),
        Item={"ShortURL": {"S": short_url}, "FullURL": {"S": long_url}},
    )

    message = {"short_url": short_url}
    return message


def handler(event, context):
    # Redirect to main page by default
    response = {
        "headers": {"Location": "/"},
        "statusCode": 301,
    }

    if event["requestContext"]["http"]["method"] == "GET":
        short_url = read_short_url(event["rawPath"][1:])
        if short_url:
            response["headers"] = {"Location": short_url}

    elif (
        event["requestContext"]["http"]["method"] == "POST"
        and event["rawPath"] == "/post/"
    ):
        success = True
        body = json.loads(event["body"])
        if "long_url" in body:
            message = write_short_url(body["long_url"])
        else:
            success, message = False, "Missing body"

        response = {
            "statusCode": 200,
            "body": json.dumps({"success": success, "message": message}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
        }

    return response
