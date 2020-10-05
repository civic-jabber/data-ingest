import newspaper
import pytest


import data_ingest.external_services.newspaper as np
import data_ingest.utils.database as db


class MockConnection:
    closed = 1


class MockArticle:
    title = "Parrots are on the loose!"
    text = "Look at all of the parrots that are flapping around."
    summary = "Look at all of the parrots that are flapping around."
    keywords = ["parrots", "flapping"]
    images = {"parrots.com/tiki.jpg"}
    url = "parrots.com"

    def build(self):
        pass


class MockPaper:
    brand = "Parrot News"
    description = "A newspaper for parrots"
    articles = [MockArticle(), MockArticle(), MockArticle()]

    def build(self):
        pass


def test_load_news_runs(monkeypatch):
    monkeypatch.setattr(newspaper, "build", lambda url: MockPaper())
    monkeypatch.setattr(db, "insert_obj", lambda *args, **kwargs: "inserted")
    monkeypatch.setattr(db, "connect", lambda *args, **kwargs: MockConnection())

    np.load_news()
