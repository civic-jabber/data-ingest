from dataclasses import dataclass
import datetime
import uuid

from civic_jabber_ingest.models.base import DataModel


@dataclass
class Article(DataModel):
    id: str = uuid.uuid4().hex
    extraction_date: datetime.datetime = datetime.datetime.now()

    source_id: str = None
    source_name: str = None
    source_brand: str = None
    source_description: str = None

    title: str = None
    body: str = None
    summary: str = None
    keywords: list = None
    images: list = None
    url: str = None
