import newspaper
import requests

import civic_jabber_ingest.external_services.newspaper as np
import civic_jabber_ingest.utils.config as config
import civic_jabber_ingest.utils.database as db


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


MOCK_CONFIG = [
    {
        "id": "0214d76dbaf640a18f86cfc443148b3d",
        "name": "News-Virginian",
        "states": ["va"],
        "url": "http://www.newsvirginian.com/",
    },
    {
        "id": "1678904925214a09bcf913cae4ead834",
        "name": "Virginia Gazette",
        "states": ["va"],
        "url": "http://www.vagazette.com/",
    },
]


def test_load_news_runs(monkeypatch):
    monkeypatch.setattr(newspaper, "build", lambda url: MockPaper())
    monkeypatch.setattr(db, "insert_obj", lambda *args, **kwargs: "inserted")
    monkeypatch.setattr(db, "connect", lambda *args, **kwargs: MockConnection())
    monkeypatch.setattr(config, "read_config", lambda *args, **kwargs: MOCK_CONFIG)

    np.load_news("va")


MOCK_USNPL_HOME = """
<html>
    <div class="row desktop">
        <a href="/search/state?state=ID">Idaho</a><br>
        <a href="/search/state?state=IL">Illinois</a><br>
    </div>
</html>
"""

MOCK_SOURCES = [
    {"id": "1", "name": "parrot news", "url": "parrots.com", "states": ["va"]},
    {"id": "2", "name": "dog news", "url": "dogs.com", "states": ["va"]},
]


def test_find_sources(monkeypatch):
    class MockResponse:
        text = MOCK_USNPL_HOME
        status_code = 200

    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: MockResponse())
    monkeypatch.setattr(np, "_state_sources", lambda state_code: MOCK_SOURCES)

    sources = np.find_sources(sleep_time=0)
    assert len(sources) == 4


MOCK_USNPL_STATE = """
<html>
    <table class="table table-sm">
        <tr>
            <td>Birdtown, USA</td>
        </tr>
        <tr>
            <td class="w-50">The Parrot Press</td>
            <td class="w-10"><a href="parrotpress.com">Link</a></td>
        </tr>
        <tr>
            <td class="w-50">The Dog Press</td>
            <td class="w-10"><a href="dogpress.com">Link</a></td>
        </tr>
    </table>
</html>
"""


def test_state_sources(monkeypatch):
    class MockResponse:
        text = MOCK_USNPL_STATE
        status_code = 200

    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: MockResponse())

    sources = np._state_sources("VA")

    assert len(sources) == 2

    assert sources[0]["name"] == "The Parrot Press"
    assert sources[0]["url"] == "parrotpress.com"
    assert sources[0]["states"] == ["va"]

    assert sources[1]["name"] == "The Dog Press"
    assert sources[1]["url"] == "dogpress.com"
    assert sources[1]["states"] == ["va"]
