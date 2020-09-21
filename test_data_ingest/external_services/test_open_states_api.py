import pytest

import data_ingest.external_services.open_states as open_states
from data_ingest.utils.environ import modified_environ


def test_session_connects_with_api_key():
    with modified_environ(**{"OPEN_STATES_API_KEY": "fake-key"}):
        session = open_states.OpenStatesSession()


def test_session_connects_with_api_key_kwarg():
    session = open_states.OpenStatesSession(api_key="fake-key")


def test_session_raises_with_no_api_key():
    with modified_environ("OPEN_STATES_API_KEY"):
        with pytest.raises(ValueError):
            session = open_states.OpenStatesSession()


class MockResponse:
    def __init__(self, status_code):
        self.status_code = 200

    def json(self):
        return {
            "results": [
                {
                    "id": "ocd-person/e0cfd740-bdcc-4644-a93b-b7cbb6cbd027",
                    "name": "Alex Q. Askew",
                    "party": "Democratic",
                    "current_role": {
                        "title": "Delegate",
                        "org_classification": "lower",
                        "district": "85",
                        "division_id": "ocd-division/country:us/state:va/sldl:85",
                    },
                    "jurisdiction": {
                        "id": "ocd-jurisdiction/country:us/state:va/government",
                        "name": "Virginia",
                        "classification": "state",
                    },
                    "given_name": "",
                    "family_name": "",
                    "image": "http://memdata.virginiageneralassembly.gov/images/display_image/H0311",
                    "gender": "",
                    "birth_date": "",
                    "death_date": "",
                    "extras": {},
                    "created_at": "2020-01-08T23:17:09.273395+00:00",
                    "updated_at": "2020-09-12T05:21:44.727872+00:00",
                },
                {
                    "id": "ocd-person/ed935430-db59-4962-91f7-c0eeca2ef8e2",
                    "name": "Alfonso H. Lopez",
                    "party": "Democratic",
                    "current_role": {
                        "title": "Delegate",
                        "org_classification": "lower",
                        "district": "49",
                        "division_id": "ocd-division/country:us/state:va/sldl:49",
                    },
                    "jurisdiction": {
                        "id": "ocd-jurisdiction/country:us/state:va/government",
                        "name": "Virginia",
                        "classification": "state",
                    },
                    "given_name": "Alfonso H.",
                    "family_name": "Lopez",
                    "image": "http://memdata.virginiageneralassembly.gov/images/display_image/H0239",
                    "gender": "Male",
                    "birth_date": "",
                    "death_date": "",
                    "extras": {},
                    "created_at": "2018-10-18T16:13:13.773120+00:00",
                    "updated_at": "2020-09-12T05:21:45.292773+00:00",
                },
            ],
            "pagination": {"per_page": 2, "page": 2, "max_page": 2, "total_items": 141},
        }


def test_get_all_people():
    open_states.Session.request = lambda self, method, url, *args, **kwargs: MockResponse(
        200
    )
    people = open_states.get_all_people("va", links=True)
    assert len(people) == 4
