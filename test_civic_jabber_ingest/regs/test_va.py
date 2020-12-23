import os

import requests
import pytest

from civic_jabber_ingest.models.title import Title
import civic_jabber_ingest.regs.va as regs
import civic_jabber_ingest.external_services.aws as aws
import civic_jabber_ingest.utils.database as database
from civic_jabber_ingest.utils.environ import modified_environ


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
    assert volumes == {("35", "6"), ("35", "5"), ("34", "1")}


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
    <div id="ContentPlaceHolder1_divTitle" class="titleDescription">TITLE 4. CONSERVATION AND NATURAL RESOURCES</div>
    <div id="ContentPlaceHolder1_divDescription" class="chapDescription">MARINE RESOURCES COMMISSION</div>
    <div id="ContentPlaceHolder1_divChapter" class="chapDescription">Chapter 252</div>
    <div id="ContentPlaceHolder1_divStatus" class="statusDescription">Final Regulation</div>
    <p class="notice0"><u>REGISTRAR'S NOTICE:</u> Be aware of the notice!</p>
    <p class="textbl"><u>Titles of Regulations</b></p>
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
    <p class="sectind0">A<s>n</s> good<s><u>outstanding</u></s></p>
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
        "chapter": "Chapter 252",
        "chapter_description": "MARINE RESOURCES COMMISSION",
        "status": "Final Regulation",
        "title": "TITLE 4. CONSERVATION AND NATURAL RESOURCES",
        "notice": "<u>REGISTRAR'S NOTICE:</u> Be aware of the notice!",
        "issue": "14",
        "volume": "19",
        "content": {
            "VA-001": {
                "code": "Good Reg",
                "description": "A<s>n</s> good<s><u>outstanding</u></s> reg",
            },
            "VA-002": {"code": "Bad Reg", "description": "A bad reg"},
        },
        "summary": "A wonderful summary!",
        "preamble": "A wonderful preamble!",
        "titles": [
            {"code": "VA-001", "description": "Fish"},
            {"code": "VA-002", "description": "Lobsters"},
        ],
        "contact": "Jabber Robinson, jabber@robinson.com",
        "authority": "Parrot law, subsection 4",
        "date": "June 08, 2020",
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
            "code": "11VAC10-120",
            "description": "Claiming Races (amending 11VAC10-120-50)",
        }
    ],
    "authority": "§ 59.1-369 of the Code of Virginia.",
    "contact": "Kimberly Mackey, Regulatory Coordinator",
    "register_date": "August 03, 2020",
    "date": "July 27, 2020.",
    "link": "http://register.dls.virginia.gov/details.aspx?id=8112",
}


def test_normalize_regulation():
    normalized_reg = regs.normalize_regulation(MOCK_REGULATION)
    assert isinstance(normalized_reg, regs.Regulation)


def test_load_va_regulations(tmpdir, monkeypatch):
    mock_loaded_issues = {("01", "01"), ("01", "02")}
    mock_listed_issues = {("01", "01"), ("01", "02"), ("02", "01")}
    mock_issue_ids = ["1111", "2222"]

    monkeypatch.setattr(regs, "get_issue_ids", lambda volume, issue: mock_issue_ids)
    monkeypatch.setattr(regs, "get_regulation", lambda issue_id: MOCK_REGULATION)
    monkeypatch.setattr(regs, "_get_loaded_issues", lambda **kwargs: mock_loaded_issues)
    monkeypatch.setattr(aws, "sync_state", lambda *args: True)
    monkeypatch.setattr(
        regs, "list_all_volumes", lambda *args, **kwargs: mock_listed_issues
    )

    env = {"CIVIC_JABBER_DATA_DIR": tmpdir.dirname}
    with modified_environ(**env):
        regs.load_va_regulations(sleep_time=0, source="aws")

    assert os.path.exists(f"{tmpdir.dirname}/regs/va/02/01/1111.xml")
    assert os.path.exists(f"{tmpdir.dirname}/regs/va/02/01/2222.xml")


def test_load_va_regulations_with_postgres(tmpdir, monkeypatch):
    mock_loaded_issues = {("01", "01"), ("01", "02")}
    mock_listed_issues = {("01", "01"), ("01", "02"), ("02", "01")}
    mock_issue_ids = ["1111", "2222"]

    monkeypatch.setattr(regs, "get_issue_ids", lambda volume, issue: mock_issue_ids)
    monkeypatch.setattr(regs, "get_regulation", lambda issue_id: MOCK_REGULATION)
    monkeypatch.setattr(regs, "_get_loaded_issues", lambda **kwargs: mock_loaded_issues)
    monkeypatch.setattr(database, "connect", lambda *args, **kwargs: True)
    monkeypatch.setattr(database, "insert_obj", lambda *args, **kwargs: True)
    monkeypatch.setattr(
        regs, "list_all_volumes", lambda *args, **kwargs: mock_listed_issues
    )

    regs.load_va_regulations(sleep_time=0, source="postgres")


def test_get_loaded_issues(tmpdir):
    os.mkdir(f"{tmpdir.dirname}/va")
    os.mkdir(f"{tmpdir.dirname}/va/01")
    os.mkdir(f"{tmpdir.dirname}/va/02")
    os.mkdir(f"{tmpdir.dirname}/va/03")
    os.mkdir(f"{tmpdir.dirname}/va/01/01")
    os.mkdir(f"{tmpdir.dirname}/va/01/02")
    os.mkdir(f"{tmpdir.dirname}/va/02/01")
    os.mkdir(f"{tmpdir.dirname}/va/03/01")

    env = {"CIVIC_JABBER_DATA_DIR": tmpdir.dirname}
    with modified_environ(**env):
        loaded_issues = regs._get_loaded_issues(tmpdir.dirname, source="local")
        assert loaded_issues == {("01", "01"), ("01", "02"), ("02", "01"), ("03", "01")}


def test_get_loaded_issues_from_aws(monkeypatch):
    mock_files = ["va/30/12/131.xml", "va/30/12/132.xml", "va/31/01/134.xml"]
    monkeypatch.setattr(aws, "s3_ls", lambda **kwargs: mock_files)
    loaded_issues = regs._get_loaded_issues(source="aws")
    assert loaded_issues == {("30", "12"), ("31", "01")}


def test_get_loaded_issues_from_postgres(monkeypatch):
    mock_issues = [("30", "12"), ("31", "01")]
    monkeypatch.setattr(database, "execute_sql", lambda *args, **kwargs: mock_issues)
    loaded_issues = regs._get_loaded_issues(source="postgres", connection="connection")
    assert loaded_issues == set(mock_issues)


def test_get_loaded_issues_raises_with_bad_option():
    with pytest.raises(ValueError):
        regs._get_loaded_issues(source="koalas")


def test_parse_contact():
    example = "Jenn Parsons, 215-867-5309, jann@jenn.com"
    first_name, last_name, email, phone = regs._parse_contact(example)
    assert first_name == "Jenn"
    assert last_name == "Parsons"
    assert email == "jann@jenn.com"
    assert phone == "215-867-5309"


def test_regs_to_titles():
    reg = {
        "issue": "09",
        "volume": "35",
        "notice": None,
        "content": {},
        "summary": None,
        "preamble": None,
        "status": "Notice of Extension of Emergency Regulation",
        "title": "TITLE 12. HEALTH",
        "chapter": "Chapter 130",
        "chapter_description": "DEPARTMENT OF MEDICAL ASSISTANCE SERVICES",
        "titles": [
            {
                "code": "12VAC30-10",
                "description": "State Plan under  Title XIX of the Social Security Act Medical Assistance Program; General  Provisions (amending 12VAC30-10-540)",
            },
            {
                "code": "12VAC30-50",
                "description": "Amount, Duration, and Scope of Medical and  Remedial Care Services (amending 12VAC30-50-130)",
            },
            {
                "code": "12VAC30-60",
                "description": "Standards Established and Methods Used to Assure  High Quality Care (amending 12VAC30-60-5, 12VAC30-60-50,  12VAC30-60-61)",
            },
            {
                "code": "12VAC30-130",
                "description": "Amount, Duration, and Scope of Selected  Services (amending 12VAC30-130-3000; repealing  12VAC30-130-850 through 12VAC30-130-890, 12VAC30-130-3020)",
            },
        ],
        "authority": "§ 32.1-325 of the Code of  Virginia; 42 USC § 1396 et seq.",
        "contact": "Emily McClellan, Regulatory Supervisor,  Policy Division, Department of Medical Assistance Services, 600 East Broad  Street, Suite 1300, Richmond, VA 23219, telephone (804) 371-4300, FAX (804)  786-1680, or email emily.mcclellan@dmas.virginia.gov.",
        "register_date": "December 24, 2018",
        "date": "June 30, 2019.",
        "state": "va",
        "link": "http://register.dls.virginia.gov/details.aspx?id=7263",
    }
    titles = regs.reg_to_titles(reg)
    assert len(titles) == 4
    assert all([isinstance(title, Title) for title in titles])
