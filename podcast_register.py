import json
import boto3
from urllib.parse import unquote_plus
import uuid
from mp3_tagger import MP3File
from pathlib import Path


s3_client = boto3.client('s3')


def main(event, context):
    response = []

    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])
        tmpkey = key.replace('/', '')
        download_path = '/tmp/{}{}'.format(uuid.uuid4(), tmpkey)
        s3_client.download_file(bucket, key, download_path)
        response.append(extract_metadata(download_path, key))

    body = {
        "message": "Registering podcast!",
        "input": event,
        "response": response
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response


def extract_metadata(file_path, key):
    mp3 = MP3File(file_path)

    dynamodb = boto3.resource('dynamodb', region_name='sa-east-1')

    table = dynamodb.Table('tablename')  # configurar o nome da tabela
    file_size = Path(file_path).stat().st_size

    return table.put_item(
        Item={
            'id': mp3.song[0].value[1:2],
            'info': {
                'episodio': mp3.song[0].value,
                'descricao': mp3.comment[0].value,
                'ano': mp3.year[0].value,
                'arquivo': {
                    'nome': key,
                    'tamanho': file_size
                }
            }
        }
    )
