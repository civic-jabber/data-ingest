from dataclasses import dataclass

from data_ingest.models.base import DataModel


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
