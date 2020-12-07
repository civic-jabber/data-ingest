import os
import pathlib

from jinja2 import Environment, FileSystemLoader, select_autoescape
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


def validate_xml(string, schema_name):
    """Validates an XML string against the specified schema.

    Parameters
    ----------
    string : str
        The XML represented as a string
    schema_name : str
        The name of the schema

    Returns
    -------
    valid : bool
        True if the XML is valid, else False
    """
    try:
        read_xml(string, schema_name)
        return True
    except etree.XMLSyntaxError:
        return False


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


def get_jinja_env():
    """Returns the Jinja environment for XML templating

    Returns
    --------
    env : jinja2.Environment
    """
    return Environment(
        loader=FileSystemLoader(searchpath=SCHEMA_DIR),
        autoescape=select_autoescape(["xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=False,
    )


def get_jinja_template(template_name):
    """Loads a jinja template from the schemas directory

    Parameters
    ----------
    template_name : str
        The name of the XML template to load

    Returns
    -------
    template : jinja2.Template
    """
    env = get_jinja_env()
    return env.get_template(f"{template_name}.xml")
