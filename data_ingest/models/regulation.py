from dataclasses import dataclass
import datetime
import uuid

from data_ingest.models.base import DataModel
from data_ingest.utils.xml import get_jinja_template


@dataclass
class Regulation(DataModel):
    id: str = uuid.uuid4().hex
    state: str = None
    issue: str = None
    volume: str = None

    notice: str = None
    regulation_number: str = None
    description: str = None
    summary: str = None
    preamble: str = None
    body: str = None

    status: str = None
    title: str = None
    chapter: str = None
    chapter_description: str = None
    titles: list = None
    authority: str = None
    contacts: list = None

    register_date: datetime.datetime = None
    effective_date: datetime.datetime = None
    as_of_date: datetime.datetime = datetime.datetime.now()

    link: str = None

    extra_attributes: dict = None

    def xml_template(self):
        data = self.to_dict(drop_empty=True)
        template = get_jinja_template("regulation")
        return template.render(data=data).strip()
