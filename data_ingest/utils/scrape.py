import re

from bs4 import BeautifulSoup
import requests


def get_page(url, **kwargs):
    """Pulls in the HTML from a URL and returns the results as a BeautifulSoupt object.

    Parameters
    ----------
    url : str
        The URL to scrape


    Returns
    -------
    soup : bs4.BeautifulSoup
        The BeautifulSoup representation of the webpage
    """
    response = requests.get(url, **kwargs)
    if response.status_code != 200:
        raise RuntimeError(
            f"Response from {url} failed with status code " "{response.status_code}"
        )
    else:
        return BeautifulSoup(response.text, "lxml")


def clean_whitespace(text):
    """Replace whitespace characters with a simple space.

    Parameters
    ----------
    text : str
        The text to clean

    Returns
    -------
    clean_text : str
        The text with whitespace replaced
    """
    return re.sub(r"\s", " ", text.strip())
