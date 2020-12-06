import datetime

from data_ingest.models.contact import Contact
from data_ingest.models.regulation import Regulation


MOCK_REGULATION = {
    "id": "1",
    "chapter": "Chapter 4",
    "chapter_description": "Fish regulations",
    "notice": "Notice: this is a great reg!",
    "title": "14-1831",
    "status": "Final Regulation",
    "state": "VA",
    "issue": "14",
    "volume": "19",
    "regulation_number": "VA-001",
    "description": "The best reg ever!",
    "body": "You <s>really</s> don't want to read this whole thing ...",
    "summary": "This is such a great reg",
    "preamble": "This is such a great reg",
    "titles": [{"title": "VA-001", "description": "Fish"}],
    "contacts": [Contact.from_dict({"first_name": "Jabber", "last_name": "Robinson"})],
    "authority": "Parrot law, subsection 4",
    "effective_date": datetime.datetime(2020, 6, 8),
    "register_date": datetime.datetime(2020, 7, 20),
    "as_of_date": datetime.datetime(2020, 8, 4),
    "link": "https://thebestregs.com",
    "extra_attributes": dict(),
}


REGULATION_XML = """
<regulation>
  <state>VA</state>
  <issue>14</issue>
  <volume>19</volume>
  <notice>Notice: this is a great reg!</notice>
  <effectiveDate>2020-06-08</effectiveDate>
  <link>https://thebestregs.com</link>
  <status>Final Regulation</status>
  <chapter>Chapter 4</chapter>
  <chapterDescription></chapterDescription>
  <title>14-1831</title>
<titles>
  <title>
    <code>VA-001</code>
    <description>Fish</description>
  </title>
</titles>
  <statuatoryAuthority>Parrot law, subsection 4</statuatoryAuthority>
  <description>The best reg ever!</description>
  <preamble>This is such a great reg</preamble>
  <summary>This is such a great reg</summary>
  <body>
    You <s>really</s> don't want to read this whole thing ...
  </body>
<contacts>
  <contact>
<firstName>Jabber</firstName>
<lastName>Robinson</lastName>
  </contact>
</contacts>
</regulation>
""".strip()


def test_regulation_loads_from_dict():
    regulation = Regulation.from_dict(MOCK_REGULATION)
    assert regulation.to_dict() == MOCK_REGULATION


def test_regulation_builds_xml():
    regulation = Regulation.from_dict(MOCK_REGULATION)
    assert regulation.xml_template() == REGULATION_XML
