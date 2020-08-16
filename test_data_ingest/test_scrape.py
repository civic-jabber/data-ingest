from bs4 import BeautifulSoup
import pytest
import requests

import data_ingest.scrape as scrape


class MockResponse:
    text = """
        <html>
            <h1>This is a wonderful site!</h1>
            <p>Look at this lovely paragraph</p>
        </html>
    """

    def __init__(self, status_code):
        self.status_code = status_code


def test_get_page_returns_bs4_object(monkeypatch):
    monkeypatch.setattr(requests, "get", lambda x: MockResponse(200))
    result = scrape.get_page("https://fake.page")
    assert isinstance(result, BeautifulSoup)


def test_get_page_raises_with_bad_status_code(monkeypatch):
    monkeypatch.setattr(requests, "get", lambda x: MockResponse(500))
    with pytest.raises(RuntimeError):
        result = scrape.get_page("https://fake.page")
