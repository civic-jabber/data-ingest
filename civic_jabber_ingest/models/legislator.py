from dataclasses import dataclass
import datetime
import uuid

from civic_jabber_ingest.models.base import DataModel


@dataclass
class Legislator(DataModel):
    id: str = uuid.uuid4().hex

    name: str = None
    given_name: str = None
    family_name: str = None
    gender: str = None

    current_state: str = None
    current_party: str = None
    current_district: str = None
    current_chamber: str = None

    links: str = None
    image: str = None
    twitter: str = None
    capitol_email: str = None
    district_email: str = None

    as_of_date: datetime.datetime = datetime.datetime.now()
