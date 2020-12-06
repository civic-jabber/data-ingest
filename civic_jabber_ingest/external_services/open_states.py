import dataclasses
import os
import urllib

import pandas as pd
from requests import Session
import tqdm

from civic_jabber_ingest.models.legislator import Legislator
import civic_jabber_ingest.utils.database as db
from civic_jabber_ingest.utils.config import read_config


_connection = None


def _connect():
    global _connection
    if not _connection or _connection.closed > 0:
        _connection = db.connect()


class OpenStatesSession(Session):
    """Base class for making API calls from across REST APIs."""

    base_url = "https://v3.openstates.org/"

    def __init__(self, api_key=None):
        super().__init__()

        api_key = api_key if api_key else os.environ.get("OPEN_STATES_API_KEY")
        if not api_key:
            raise ValueError(
                "The API key must be specified in the api_key argument or "
                "using the OPEN_STATES_API_KEY environment variable. "
            )
        self.headers.update({"X-API-KEY": api_key})

    def __str__(self):
        return self.__class__.__name__

    def request(self, method, url, *args, **kwargs):
        url = self._create_url(url)
        return super().request(method, url, *args, **kwargs)

    def _create_url(self, url):
        if not self.base_url:
            raise ValueError("Base URL for the external service has not been set.")
        return f"{self.base_url}{url}"


def get_jurisdiction_id(state_code):
    return f"ocd-jurisdiction/country:us/state:{state_code.lower()}/government"


def get_all_people(state_code, per_page=10, links=False):
    """Pulls a list of all of the legislators for the specified state

    Parameters
    ----------
    state_code : str
        The two letter state code for the state
    per_page : int
        The number of results per page
    links : bool
        If True, also include links

    Returns
    -------
    people : list
        A list of all the legislators as their information
    """
    kwargs = {"state_code": state_code, "per_page": per_page, "links": links}
    response = get_people(**kwargs, page=1)
    max_page = response["pagination"]["max_page"]
    people = response["results"]

    if max_page > 1:
        for page in tqdm.tqdm(range(2, max_page + 1)):
            response = get_people(**kwargs, page=page)
            people.extend(response["results"])
    return people


def get_people(state_code, page, per_page=10, links=False):
    """Pulls a list of all of the legislators for the specified state

    Parameters
    ----------
    state_code : str
        The two letter state code for the state
    page : int
        The the page to pull
    per_page : int
        The number of results per page
    links : bool
        If True, also include links

    Returns
    -------
    response : dict
        The dictionary response for the API call
    """
    session = OpenStatesSession()
    params = {
        "jurisdiction": get_jurisdiction_id(state_code),
        "page": page,
        "per_page": per_page,
    }
    if links:
        params["include"] = "links"

    response = session.get(f"people?{urllib.parse.urlencode(params)}")
    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError(
            f"Open States API call failed with status code: {response.status_code}."
        )


LEGISLATOR_BASE_URL = "https://data.openstates.org/people/current"
LEGISLATOR_FIELDS = set(f.name for f in dataclasses.fields(Legislator))


def update_legislators():
    """Updates all of the legislators in the database."""
    states = read_config("states")
    for state in tqdm.tqdm(states.keys()):
        legislator_csv_to_db(state)


def legislator_csv_to_db(state):
    """Pulls the latest list of legislators from OpenStates and updates the CivicJabber
    database accordingly.

    Parameters
    ----------
    state : str
        The two letter code for the state. Case insensitive.
    """
    _connect()
    state = state.lower()
    url = f"{LEGISLATOR_BASE_URL}/{state}.csv"
    try:
        legislators = pd.read_csv(url)
    except urllib.error.URLError:
        return
    # Replaces NaN values with None
    legislators = legislators.where(pd.notnull(legislators), None)
    legislators["current_state"] = state

    for i in legislators.index:
        legislator = dict(legislators.loc[i])
        legislator["current_district"] = str(legislator["current_district"])
        for key in list(legislator.keys()):
            if key not in LEGISLATOR_FIELDS:
                del legislator[key]
        legislator = Legislator.from_dict(legislator)

        db.delete_by_id(legislator.id, table="legislators", connection=_connection)
        db.insert_obj(legislator, table="legislators", connection=_connection)
