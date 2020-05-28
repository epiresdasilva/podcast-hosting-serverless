import boto3
from podgen import Podcast, Episode, Media, Person

s3_client = boto3.client('s3')


def main(event, context):
    dynamodb = boto3.resource('dynamodb', region_name='sa-east-1')

    table = dynamodb.Table('tablename')  # configurar o nome da tabela

    podcasts = table.scan()

    author = Person("Nome completo", "seu@email.com.br")
    p = Podcast(
        name="Nome do podcast",
        description="Descrição completa do podcast.",
        website="https://seupodcast.com.br",
        explicit=False,
        copyright="2020 Nome completo",
        language="pt-BR",
        authors=[author],
        feed_url="https://URL_API_GATEWAY/dev/podcasts/rss",  # configurar a URL gerada para o API gateway
        owner=author,
        image="http://seupodcast.com.br/logo.jpg",
        web_master=Person(None, "seu@email.com.br")
    )

    items = podcasts['Items']
    for item in items:
        base_url = "http://URL_BASE_CLOUDFRONT/"  # configurar a URL gerada no CloudFront
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
