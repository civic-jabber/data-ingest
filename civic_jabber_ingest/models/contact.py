from dataclasses import dataclass

from civic_jabber_ingest.models.base import DataModel
from civic_jabber_ingest.utils.xml import get_jinja_template


@dataclass
class Contact(DataModel):
    first_name: str = None
    last_name: str = None
    agency: str = None
    address: str = None
    city: str = None
    state: str = None
    zip_code: str = None
    phone: str = None
    email: str = None

    def xml_template(self):
        data = self.to_dict(drop_empty=True)
        template = get_jinja_template("contact")
        return template.render(data=data).strip()
