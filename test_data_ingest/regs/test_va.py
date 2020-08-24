from bs4 import BeautifulSoup
import requests

import data_ingest.regs.va as regs


TEST_ARCHIVE = """
<html>
    <div class="archiveDetail">
        <a href="=35:6">Vol 35, Issue 6</a>
        <a href="=a:b">PDF</a>
    </div>
    <div class="archiveDetail">
        <a href="=35:5">Vol 35, Issue 5</a>
        <a href="=a:b">PDF</a>
    </div>
    <div class="archiveDetail">
        <a href="=34:1">Vol 34, Issue 1</a>
        <a href="=a:b">PDF</a>
    </div>
</html>
"""


def test_list_all_volumes(monkeypatch):
    class MockResponse:
        text = TEST_ARCHIVE
        status_code = 200

    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: MockResponse())
    volumes = regs.list_all_volumes()
    assert volumes == {"35": ["6", "5"], "34": ["1"]}


TEST_ISSUE = """
<html>
    <div id="ContentPlaceHolder1_divRegs">
        <a href="issue32">Issue 32</a>
        <a href="details?id=8801">A regulation</a>
        <a href="details?id=8802">Another regulation</a>
    </div>
</html>
"""


def test_get_issue(monkeypatch):
    class MockResponse:
        text = TEST_ISSUE
        status_code = 200

    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: MockResponse())
    regulation_ids = regs.get_issue_ids("fake_issue", "fake_volume")
    assert regulation_ids == ["8801", "8802"]


TEST_REGULATION = """
<html>
    <div class="currentIssue-DateIssue">Vol. 19 Iss. 14 - June 01, 2020</div>
    <p class="textbl"><u>Titles of Regulations</b></p>
    <p class="textbl"><b> VA-001. Fish</b></p>
    <p class="textbl"><strong> VA-002. Lobsters</strong></p>
    <p class="textbl">
        <span>Effective Date</span>
        <span>June 08, 2020</span>
    </p>
    <p class="textbl">
        <span>Agency Contact</span>
        Jabber Robinson
    </p>
    <p class="textbl">
        <span>Statuatory Authority</span>
        <span>Parrot law, subsection 4</span>
    </p>
    <p class="summary">Summary</p>
    <p>This is such a great reg</p>
    <p class="vacno0">VA-001. Good Reg</p>
    <p class="sectind0">A good</p>
    <p class="sectind0">reg</p>
    <p class="vacno0">VA-002. Bad Reg</p>
    <p class="sectind0">A bad</p>
    <p class="sectind0">reg</p>
    <p>Skip me</p>
</html>
"""


def test_get_regulation(monkeypatch):
    class MockResponse:
        text = TEST_REGULATION
        status_code = 200

    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: MockResponse())

    regulation = regs.get_regulation("fake_id")
    assert regulation == {
        "titles": [
            {"title": "VA-001", "description": "Fish"},
            {"title": "VA-002", "description": "Lobsters"},
        ],
        "summary": "This is such a great reg",
        "effective_date": "June 08, 2020",
        "contact": "Jabber Robinson",
        "authority": "Parrot law, subsection 4",
        "date": "June 01, 2020",
        "issue": "14",
        "volume": "19",
        "content": {
            "VA-001": {"description": "Good Reg", "text": "A good reg"},
            "VA-002": {"description": "Bad Reg", "text": "A bad reg"},
        },
    }
