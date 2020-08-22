from data_ingest.models.regulation import Regulation
from data_ingest.utils.scrape import get_page


VA_REGISTRY_PAGE = "http://register.dls.virginia.gov/archive.aspx"
VA_REG_TEMPLATE = "http://register.dls.virginia.gov/toc.aspx?voliss={vol}:{issue}"
VA_REGULATION = "http://register.dls.virginia.gov/details.aspx?id={site_id}"


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


class VirginiaRegulation(Regulation):
    """Pulls structured information about a regulation from the Virginia Registry
    website."""

    def __init__(self, site_id):
        url = VA_REGULATION.format(site_id=site_id)
        self.html = get_page(url)
