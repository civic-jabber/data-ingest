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
