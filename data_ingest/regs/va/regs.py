from data_ingest.utils.scrape import get_page


VA_REGISTRY_PAGE = "http://register.dls.virginia.gov/archive.aspx"


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
