from dataclasses import dataclass
import datetime
import uuid

from civic_jabber_ingest.models.base import DataModel


@dataclass
class Title(DataModel):
    id: str = uuid.uuid4().hex
    state: str = None
    issue: str = None
    volume: str = None

    title: str = None
    description: str = None
    summary: str = None
    status: str = None
    link: str = None

    register_date: datetime.datetime = None
    date: datetime.datetime = None
    start_date: datetime.datetime = None
    end_date: datetime.datetime = None
    as_of_date: datetime.datetime = datetime.datetime.now()
