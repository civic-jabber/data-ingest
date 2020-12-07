import datetime

from civic_jabber_ingest.models.legislator import Legislator


MOCK_LEGISLATOR = {
    "id": "ocd-person/5a26eb7c-86d1-415a-8b1e-ba64dc25b611",
    "name": 'A. Benton "Ben" Chafin',
    "current_state": "VA",
    "current_party": "Republican",
    "current_district": 38,
    "current_chamber": "upper",
    "given_name": 'A. Benton "Ben"',
    "family_name": "Chafin",
    "gender": "Male",
    "image": "https://apps.lis.virginia.gov/senatepics/newbiopics/Chafin38.jpg",
    "links": "http://lis.virginia.gov/cgi-bin/legp604.exe?191+mbr+S93",
    "capitol_email": None,
    "district_email": "district38@senate.virginia.gov",
    "twitter": "chafin4senate",
    "as_of_date": datetime.datetime(2020, 10, 4),
}


def test_legislator():
    legislator = Legislator.from_dict(MOCK_LEGISLATOR)
    assert legislator.to_dict() == MOCK_LEGISLATOR
