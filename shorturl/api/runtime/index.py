import json
import boto3
import os
import random
import string


client = boto3.client("dynamodb")


def handler(event, context):
    data = {}
    response = {
        "headers": {"Location": "/"},
        "statusCode": 301,
    }

    if event["requestContext"]["http"]["method"] == "GET":
        data = client.get_item(
            TableName=os.getenv("DYNAMODB_TABLE_NAME"),
            Key={"ShortURL": {"S": event["rawPath"][1:]}},
        )
        if "Item" in data:
            response["headers"] = {"Location": data["Item"]["FullURL"]["S"]}

    elif (
        event["requestContext"]["http"]["method"] == "POST"
        and event["rawPath"] == "/post/"
    ):
        success = True
        body = json.loads(event["body"])
        if "long_url" in body:
            long_url = body["long_url"]
            # Create ShortURL
            short_url = "".join(random.choices(string.ascii_letters, k=4))
            # Save to DynamoDB
            data = client.put_item(
                TableName=os.getenv("DYNAMODB_TABLE_NAME"),
                Item={"ShortURL": {"S": short_url}, "FullURL": {"S": long_url}},
            )

            message = {"short_url": short_url}
        else:
            success = False
            message = "Missing body"

        response = {
            "statusCode": 200,
            "body": json.dumps({"success": success, "message": message}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
        }

    return response
