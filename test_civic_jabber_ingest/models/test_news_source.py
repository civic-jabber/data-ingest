import datetime

from civic_jabber_ingest.models.news_source import NewsSource


MOCK_NEWS_SOURCE = {
    "id": "1",
    "source_name": "Parrot News",
    "state": "va",
    "url": "https://www.birds.com/news/big-birds",
    "updated_date": datetime.datetime.now(),
}


def test_news_source_loads_from_dict():
    news_source = NewsSource.from_dict(MOCK_NEWS_SOURCE)
    assert news_source.to_dict() == MOCK_NEWS_SOURCE
