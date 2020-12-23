import datetime

from civic_jabber_ingest.models.title import Title


MOCK_TITLE = {
    "id": "1",
    "state": "va",
    "issue": "01",
    "volume": "01",
    "title": "1VA-204-23",
    "description": "Rules governing parrots",
    "summary": "Look at all the parrots!",
    "status": "Final regulation",
    "link": "www.parrotregulations.virginia",
    "register_date": datetime.datetime.today(),
    "date": datetime.datetime.today(),
    "start_date": datetime.datetime.today(),
    "end_date": datetime.datetime.today(),
    "as_of_date": datetime.datetime.today(),
}


def test_title_loads_from_dict():
    title = Title.from_dict(MOCK_TITLE)
    assert title.to_dict() == MOCK_TITLE
