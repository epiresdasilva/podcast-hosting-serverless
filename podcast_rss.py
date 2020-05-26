import boto3
from podgen import Podcast, Episode, Media, Person, Category

s3_client = boto3.client('s3')


def main(event, context):
    dynamodb = boto3.resource('dynamodb', region_name='sa-east-1')

    table = dynamodb.Table('semservidor-dev')

    podcasts = table.scan()

    author = Person("Evandro Pires da Silva", "evandro@evandropires.com.br")
    p = Podcast(
        name="Sem Servidor",
        description="Podcast dedicado a arquitetura serverless, com conteúdo de qualidade em português.",
        website="https://semservidor.com.br",
        explicit=False,
        copyright="2020 Evandro Pires da Silva",
        language="pr-BR",
        authors=[author],
        feed_url="https://3tz8r90j0d.execute-api.sa-east-1.amazonaws.com/dev/podcasts/rss",
        category=Category("Music", "Music History"),
        owner=author,
        image="http://d30gvsirhz3ono.cloudfront.net/logo_semservidor_teste.jpg",
        web_master=Person(None, "evandro@evandropires.com.br")
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
                position=int(item['id'])
            )
        ]

    p.apply_episode_order()
    rss = p.rss_str()

    response = {
        "statusCode": 200,
        "headers": {
            "content-type": "application/xml"
        },
        "body": rss
    }

    return response
