from data_ingest.models.contact import Contact


MOCK_CONTACT = {
    "first_name": "Jabber",
    "last_name": "Parrot",
    "agency": "Parrot Commission",
    "address": "123 Parrot Rd",
    "city": "Parrotville",
    "state": "PA",
    "zip_code": "22341",
    "phone": "1-800-PARROT",
    "email": "jabber@fake.email",
}


CONTACT_XML = """
<firstName>Jabber</firstName>
<lastName>Parrot</lastName>
<agency>Parrot Commission</agency>
<city>Parrotville</city>
<state>PA</state>
<zipCode>22341</zipCode>
<phone>1-800-PARROT</phone>
<email>jabber@fake.email</email>
""".strip()


def test_contact_loads_from_dict():
    contact = Contact.from_dict(MOCK_CONTACT)
    assert contact.to_dict() == MOCK_CONTACT


def test_contact_builds_xml():
    contact = Contact.from_dict(MOCK_CONTACT)
    assert contact.xml_template() == CONTACT_XML
