import os

from data_ingest.scrape import get_page


BULK_DOWNLOAD_PAGE = "https://openstates.org/data/session-csv/"


def get_bulk_download_page(cookie):
    """Pulls the bulk download page from the OpenStates website. You need to pass in
    cookies because it only shows the download urls you are logged in.

    Parameters
    ----------
    cookie : str
        The user session cookies. You can grab these from the developer tools in the
        browser

    Returns
    -------
    soup : bs4.BeautifulSoup
        A BeautifulSoup representation of the download page
    """
    return get_page(BULK_DOWNLOAD_PAGE, headers={"cookie": cookie})


def get_bulk_download_links(page):
    """Extracts the bulk download links from the BeautifulSoup object

    Parameters
    ----------
    page : bs4.BeautifulSoup
        The bs4 representation for the bulk download page

    Returns
    -------
    download_links : dict
        A dictionary containing the download links
    """
    section = page.find("section")
    links = section.find_all("a")

    download_links = dict()
    current_state = None

    for link in links:
        if "name" in link.attrs:
            current_state = link["name"]
        elif "href" in link.attrs:
            if link["href"].startswith("mailto:"):
                continue
            session = link.text.strip()
            state_links = download_links.get(current_state, list())
            state_links.append({"session": session, "link": link["href"]})
            download_links[current_state] = state_links

    return download_links
