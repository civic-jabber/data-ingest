from data_ingest.models.regulation import Regulation
from data_ingest.utils.scrape import get_page, clean_whitespace


VA_REGISTRY_PAGE = "http://register.dls.virginia.gov/archive.aspx"
VA_REG_TEMPLATE = "http://register.dls.virginia.gov/toc.aspx?voliss={vol}:{issue}"
VA_REGULATION = "http://register.dls.virginia.gov/details.aspx?id={site_id}"


class VirginiaRegulation(Regulation):
    """Pulls structured information about a regulation from the Virginia Registry
    website."""

    @classmethod
    def from_html(cls, html):
        pass


def get_regulation(site_id):
    """Pulls the html for a regulation using the site id. Note, in some cases there are
    multiple regulations addressed on a single page.

    Parameters
    ----------
    site_id : str
        The site id for the page

    Returns
    -------
    html : bs4.BeautifulSoup
        The bs4 representation for the site
    """
    url = VA_REGULATION.format(site_id=site_id)
    return get_page(url)


def _get_metadata(html):
    """Pulls metadata for the regulations that are addressed on the page.

    Parameters
    ----------
    html : bs4.BeautifulSoupt
        The bs4 representation of the site

    Returns
    -------
    metadata : dict
        A dictionary of metadata for the regulations
    """
    meta = dict()
    metadata = html.find_all("p", class_="textbl")
    meta["titles"] = _get_titles(metadata)
    return meta


def _get_titles(metadata):
    """Pulls the title and description for the regulations on the page.

    Parameters
    ----------
    metadata : bs4.BeautfiulSoup
        An html element from the header section

    Returns
    -------
    title : list
        The title of titles and descriptions
    """
    titles = list()
    for line in metadata:
        bold = line.find_all("b") + line.find_all("strong")
        text = str()
        for item in bold:
            text += item.text
        if text:
            title, description = tuple(text.split(".")[:2])
            titles.append(
                {
                    "title": clean_whitespace(title),
                    "description": clean_whitespace(description),
                }
            )
    return titles


def list_all_volumes():
    """Lists all available issues and volumes from the VA registry webpage. Only returns
    volumes that are available on HTML.

    Returns
    -------
    volumes : dict
        A dictionary where the volumes are the keys and the issues are list entries.
    """
    volumes = dict()
    html = get_page(VA_REGISTRY_PAGE)
    details = html.find_all(class_="archiveDetail")
    for line in details:
        links = line.find_all("a")
        for link in links:
            if link.text != "PDF":
                volume, issue = tuple(link["href"].split("=")[-1].split(":"))
                issues = volumes.get(volume, [])
                issues.append(issue)
                volumes[volume] = issues
                break
    return volumes


def get_issue_ids(volume, issue):
    """Pulls a list of the IDs for all of the regulations in the issue.

    Parameters
    ----------
    volume : str
        The volume to pull
    issue : str
        The issue to pull

    Returns
    -------
    regulation_ids : list
        A list of IDs for the specified volume
    """
    url = VA_REG_TEMPLATE.format(vol=volume, issue=issue)
    html = get_page(url)
    regulations = html.find("div", {"id": "ContentPlaceHolder1_divRegs"})
    links = regulations.find_all("a")
    regulation_ids = list()
    for link in links:
        if "href" in link.attrs and link["href"].startswith("details"):
            regulation_ids.append(link["href"].split("=")[-1])
    return regulation_ids
