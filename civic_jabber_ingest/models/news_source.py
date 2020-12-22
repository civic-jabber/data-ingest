from dataclasses import dataclass
import datetime
import uuid

from civic_jabber_ingest.models.base import DataModel


@dataclass
class NewsSource(DataModel):
    id: str = uuid.uuid4().hex
    source_name: str = None
    state: str = None
    url: str = None
    updated_date: str = datetime.datetime.now()
