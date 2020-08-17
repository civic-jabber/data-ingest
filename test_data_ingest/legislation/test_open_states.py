import requests

import data_ingest.legislation.open_states as open_states


class MockResponse:
    status_code = 200
    text = """
    <html>
    <h1>Look at this great page!</h1>
    <section>
        <a href="mailto:fake@fake.com">E-mail us</a>
        <a name="Alabama">Alabama</a>
        <a href="https://fake.com/file1.csv">File 1</a>
        <a href="https://fake.com/file2.csv">File 2</a>

        <a name="Pennsylvania">Pennsylvania</a>
        <a href="https://fake.com/file3.csv">File 3</a>
        <a href="https://fake.com/file4.csv">File 4</a>

    <section>
    </html>
    """


def test_get_download_links(monkeypatch):
    monkeypatch.setattr(requests, "get", lambda url, **kwargs: MockResponse())
    page = open_states.get_bulk_download_page("fake_cookies")
    links = open_states.get_bulk_download_links(page)
    assert links == {
        "Alabama": [
            {"session": "File 1", "link": "https://fake.com/file1.csv"},
            {"session": "File 2", "link": "https://fake.com/file2.csv"},
        ],
        "Pennsylvania": [
            {"session": "File 3", "link": "https://fake.com/file3.csv"},
            {"session": "File 4", "link": "https://fake.com/file4.csv"},
        ],
    }
