import os
import pathlib

from lxml import etree

PATH = pathlib.Path(__file__).parent.absolute()
SCHEMA_DIR = os.path.join(PATH, "..", "schemas")


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
