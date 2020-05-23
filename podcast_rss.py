import boto3
from podgen import Podcast, Episode, Media

s3_client = boto3.client('s3')


def main(event, context):
    dynamodb = boto3.resource('dynamodb', region_name='sa-east-1')

    table = dynamodb.Table('semservidor-dev')

    podcasts = table.scan()

    p = Podcast(
        name="Sem Servidor",
        description="A cada duas semanas um novo podcast sobre serverless em português.",
        website="https://semservidor.com.br",
        explicit=False
    )

    items = podcasts['Items']
    for item in items:
        base_url = "http://d30gvsirhz3ono.cloudfront.net/"
        file_path = base_url + item['info']['arquivo']['nome']
        p.episodes += [
            Episode(
                title=item['info']['episodio'],
                media=Media(file_path, int(item['info']['arquivo']['tamanho'])),
                summary=item['info']['descricao'],
            )
        ]

    rss = p.rss_str()

    response = {
        "statusCode": 200,
        "headers": {
            "content-type": "application/xml"
        },
        "body": rss
    }

    return response
