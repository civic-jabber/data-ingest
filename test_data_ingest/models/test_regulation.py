import datetime

from data_ingest.models.regulation import Regulation


MOCK_REGULATION = {
    "id_": "1",
    "state": "VA",
    "issue": "14",
    "volume": "19",
    "regulation_number": "VA-001",
    "description": "The best reg ever!",
    "body": "You really don't want to read this whole thing ...",
    "summary": "This is such a great reg",
    "preamble": "This is such a great reg",
    "titles": [{"title": "VA-001", "description": "Fish"}],
    "contact": "Jabber Robinson, jabber@robinson.com",
    "authority": "Parrot law, subsection 4",
    "effective_date": datetime.datetime(2020, 6, 8),
    "register_date": datetime.datetime(2020, 7, 20),
    "as_of_date": datetime.datetime(2020, 8, 4),
    "link": "https://thebestregs.com",
}


def test_regulation_loads_from_dict():
    regulation = Regulation.from_dict(MOCK_REGULATION)
    assert regulation.to_dict() == MOCK_REGULATION
