import os
import pathlib

from lxml import etree

PATH = pathlib.Path(__file__).parent.absolute()
SCHEMA_DIR = os.path.join(PATH, "..", "schemas")


def read_xml(string, schema_name):
    """Reads in XML using the specified schema

    Parameters
    ----------
    string : str
        The XML represented as a string
    schema_name : str
        The name of the schema

    Returns
    -------
    xml : etree._Element
    """
    parser = read_xsd(schema_name)
    return etree.fromstring(string, parser)


def read_xsd(schema_name):
    """Reads an XML schema from the schema directory.

    Parameters
    ----------
    schema_name : str
        The name of the schema in the schema directory

    Returns
    -------
    parser : etree.XMLParser
    """
    filename = os.path.join(SCHEMA_DIR, f"{schema_name}.xsd")
    with open(filename, "r") as f:
        schema_root = etree.XML(f.read())
    schema = etree.XMLSchema(schema_root)
    return etree.XMLParser(schema=schema)
