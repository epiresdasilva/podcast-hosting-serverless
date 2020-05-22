import json
import boto3
from urllib.parse import unquote_plus
import uuid
from mp3_tagger import MP3File


s3_client = boto3.client('s3')


def main(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])
        tmpkey = key.replace('/', '')
        download_path = '/tmp/{}{}'.format(uuid.uuid4(), tmpkey)
        s3_client.download_file(bucket, key, download_path)
        extract_metadata(download_path)

    body = {
        "message": "Registering podcast!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response


def extract_metadata(file_path):
    mp3 = MP3File(file_path)
    print(mp3.album)
