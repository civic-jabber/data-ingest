import pytest
from lxml import etree

import data_ingest.utils.xml as xml


@pytest.fixture
def valid_regulation():
    return """
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


@pytest.fixture
def invalid_regulation():
    return """
        <regulation>
            <state>VA</state>
            <issue>not an int</issue>
            <titles>
                <title>
                    <code>4VAC20-252</code>
                    <description>Parrots</description>
                </title>
                <title>
                    <code>4VAC20-254</code>
                    <description>Dogs</description>
                </title>
            </titles>
        </regulation>
    """


def test_parser_validates_valid_reg(valid_regulation):
    root = xml.read_xml(valid_regulation, "regulation")
    assert isinstance(root, etree._Element)


def test_parser_raises_on_invalid_reg(invalid_regulation):
    with pytest.raises(etree.XMLSyntaxError):
        xml.read_xml(invalid_regulation, "regulation")
