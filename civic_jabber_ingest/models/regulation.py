from dataclasses import dataclass
import datetime
import uuid

from civic_jabber_ingest.models.base import DataModel


@dataclass
class Regulation(DataModel):
    id: str = uuid.uuid4().hex
    state: str = None
    issue: str = None
    volume: str = None

    regulation_number: str = None
    description: str = None
    summary: str = None
    preamble: str = None
    body: str = None

    titles: list = None
    authority: str = None
    contact: str = None

    register_date: datetime.datetime = None
    effective_date: datetime.datetime = None
    as_of_date: datetime.datetime = datetime.datetime.now()

    link: str = None

    extra_attributes: dict = None
