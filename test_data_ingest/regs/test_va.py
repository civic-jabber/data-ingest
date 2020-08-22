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
    regulation_ids = regs.get_issue("fake_issue", "fake_volume")
    assert regulation_ids == ["8801", "8802"]
