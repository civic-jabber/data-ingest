import os
import urllib

from civic_jabber_ingest.utils.scrape import get_page


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
    """Extracts the bulk download links from the BeautifulSoup object.

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


def download_data(links, directory):
    """Downloads the OpenStates data to the specified location.

    Parameters
    ----------
    links : dict
        A dictionary containing the lines and session names
    directory : str
        The name of the directory in which to save the files
    """
    for state, session_files in links.items():
        subdirectory = os.path.join(directory, state.replace(" ", "_"))
        if not os.path.exists(subdirectory):
            print(f"Creating subdirectory: {subdirectory}")
            os.mkdir(subdirectory)

        for session_file in session_files:
            url = session_file["link"]
            if " " in url:
                print(f"Skipping invalid url: {url}")
            filename = f"{session_file['session'].replace(' ', '-')}.zip"
            destination = os.path.join(subdirectory, filename)
            if os.path.exists(destination):
                print(f"Skipping {filename}. File already exists in {subdirectory}")
            else:
                urllib.request.urlretrieve(url, destination)
                print(f"Downloading {url} to {destination}")
