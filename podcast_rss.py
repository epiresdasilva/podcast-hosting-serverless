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
        p.episodes += [
            Episode(
                title=item['info']['episodio'],
                media=Media("http://example.org/files/aardvark.mp3", 11932295),  # TODO
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
