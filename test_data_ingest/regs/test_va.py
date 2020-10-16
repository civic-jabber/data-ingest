import requests

import data_ingest.regs.va as regs
import data_ingest.utils.database as db


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
    <p class="textbl"><u>Titles of Regulation:s</b></p>
    <p class="textbl"><b> VA-001. Fish</b></p>
    <p class="textbl"><strong> VA-002. Lobsters</strong></p>
    <p class="textbl">
        <span>Effective Date:</span>
        June 08, 2020
    </p>
    <p class="textbl">
        <u>Agency Contact:</u>
        Jabber Robinson, <span>jabber@robinson.com</span>
    </p>
    <p class="textbl">
        <span>Statuatory Authority:</span>
        <span>Parrot law, subsection 4</span>
    </p>
    <p class="summary">Summary:</p>
    <p>A wonderful summary!</p>
    <p class="preamble">Preamble:</p>
    <p>A wonderful preamble!</p>
    <p class="vacno0">VA-001. Good Reg</p>
    <p class="sectind0">A<s>n</s> good<s>outstanding</s></p>
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
        "issue": "14",
        "volume": "19",
        "content": {
            "VA-001": {"description": "Good Reg", "text": "A good reg"},
            "VA-002": {"description": "Bad Reg", "text": "A bad reg"},
        },
        "summary": "A wonderful summary!",
        "preamble": "A wonderful preamble!",
        "titles": [
            {"title": "VA-001", "description": "Fish"},
            {"title": "VA-002", "description": "Lobsters"},
        ],
        "contact": "Jabber Robinson, jabber@robinson.com",
        "authority": "Parrot law, subsection 4",
        "effective_date": "June 08, 2020",
        "register_date": "June 01, 2020",
        "link": regs.VA_REGULATION.format(site_id="fake_id"),
        "state": "va",
    }


MOCK_REGULATION = {
    "issue": "25",
    "volume": "36",
    "content": {
        "11VAC10-120-50": {
            "text": "The following provisions shall apply.",
            "description": "Claiming procedure",
        }
    },
    "summary": "The amendments (i) allow for the voiding of a claim.",
    "preamble": None,
    "titles": [
        {
            "title": "11VAC10-120",
            "description": "Claiming Races (amending 11VAC10-120-50)",
        }
    ],
    "authority": "§ 59.1-369 of the Code of Virginia.",
    "contact": "Kimberly Mackey, Regulatory Coordinator",
    "register_date": "August 03, 2020",
    "effective_date": "July 27, 2020.",
    "link": "http://register.dls.virginia.gov/details.aspx?id=8112",
}


def test_normalize_regulation():
    normalized_reg = regs.normalize_regulation(MOCK_REGULATION)
    assert isinstance(normalized_reg, regs.Regulation)


def test_load_va_regulations(monkeypatch):
    mock_loaded_issues = [("1", "1"), ("1", "2")]
    mock_listed_issues = {"1": ["1", "2"], "2": ["1"]}
    mock_issue_ids = ["1111", "2222"]

    class MockConnection:
        closed = 0

    monkeypatch.setattr(db, "connect", lambda *args, **kwargs: MockConnection())
    monkeypatch.setattr(db, "insert_obj", lambda *args, **kwargs: None)
    monkeypatch.setattr(db, "execute_sql", lambda *args, **kwargs: mock_loaded_issues)
    monkeypatch.setattr(regs, "get_issue_ids", lambda volume, issue: mock_issue_ids)
    monkeypatch.setattr(regs, "get_regulation", lambda issue_id: MOCK_REGULATION)
    monkeypatch.setattr(
        regs, "list_all_volumes", lambda *args, **kwargs: mock_listed_issues
    )

    regs.load_va_regulations(sleep_time=0)
