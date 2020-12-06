import pytest
from lxml import etree

import civic_jabber_ingest.utils.xml as xml


@pytest.fixture
def valid_regulation():
    return """
        <regulation>
            <state>VA</state>
            <issue>1</issue>
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
