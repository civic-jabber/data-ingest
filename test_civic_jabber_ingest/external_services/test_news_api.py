import pytest

import civic_jabber_ingest.external_services.news_api as news_api
from civic_jabber_ingest.utils.environ import modified_environ


def test_session_connects_with_api_key():
    with modified_environ(**{"NEWS_API_KEY": "fake-key"}):
        news_api.NewsAPISession()


def test_session_connects_with_api_key_kwarg():
    news_api.NewsAPISession(api_key="fake-key")


def test_session_raises_with_no_api_key():
    with modified_environ("NEWS_API_KEY"):
        with pytest.raises(ValueError):
            news_api.NewsAPISession()


class MockResponse:
    def __init__(self, **kwargs):
        self.params = kwargs.get("params", dict())


def test_api_key_added_as_param():
    news_api.Session.request = lambda self, method, url, *args, **kwargs: MockResponse(
        **kwargs
    )
    with modified_environ(**{"NEWS_API_KEY": "fake-key"}):
        session = news_api.NewsAPISession()
    response = session.get("/parrots")
    assert response.params["apiKey"] == "fake-key"
