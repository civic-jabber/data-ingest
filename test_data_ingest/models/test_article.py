import datetime

from data_ingest.models.article import Article


MOCK_ARTICLE = {
    "id": "1",
    "extraction_date": datetime.datetime(2020, 6, 8),
    "source_id": "4",
    "source_brand": "Parrot News",
    "source_description": "A news source for parrots",
    "title": "You'll never believe the size of these parrots!",
    "text": "Parrts are big and parrts are tall!",
    "summary": "Parrts are big and parrts are tall!",
    "keywords": ["big", "parrot"],
    "images": ["big_bird.jpg", "little_bird.jpg"],
    "url": "https://www.birds.com/news/big-birds",
}


def test_article_loads_from_dict():
    article = Article.from_dict(MOCK_ARTICLE)
    assert article.to_dict() == MOCK_ARTICLE
