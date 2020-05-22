import json


def main(event, context):
    body = {
        "message": "RSS",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
