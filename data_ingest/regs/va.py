import re

from data_ingest.models.regulation import Regulation
from data_ingest.utils.scrape import get_page, clean_whitespace


VA_REGISTRY_PAGE = "http://register.dls.virginia.gov/archive.aspx"
VA_REG_TEMPLATE = "http://register.dls.virginia.gov/toc.aspx?voliss={vol}:{issue}"
VA_REGULATION = "http://register.dls.virginia.gov/details.aspx?id={site_id}"


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
    html = get_page(url)
    regulation = _parse_html(html)
    regulation["link"] = url
    return regulation


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


def _parse_html(html):
    """Pulls metadata for the regulations that are addressed on the page.

    Parameters
    ----------
    html : bs4.BeautifulSoupt
        The bs4 representation of the site

    Returns
    -------
    reg : dict
        A dictionary of metadata for the regulations
    """
    reg = dict()
    metadata = html.find_all("p", class_="textbl")
    issue, volume, date = _get_issue_data(html)

    reg["issue"] = issue
    reg["volume"] = volume

    reg["content"] = _get_regulation_content(html)
    reg["summary"] = _get_summary(html)
    reg["preamble"] = _get_summary(html, summary_class="preamble")

    reg["titles"] = _get_titles(metadata)
    reg["authority"] = _get_target_metadata(metadata, "Authority")
    reg["contact"] = _get_target_metadata(metadata, "Contact")

    reg["register_date"] = date
    reg["effective_date"] = _get_target_metadata(metadata, "Effective Date")
    return reg


def _get_regulation_content(html):
    """Pulls the regulation text from the document

    Parameters
    ----------
    html : bs4.BeautifulSoupt
        The bs4 representation of the site

    Returns
    -------
    content : dict
        A dictionary where the keys are the regulation numbers and the entries contain a
        description of the regulation and the text
    """

    def _add_reg_text(regulation, description, text):
        if regulation and description:
            content[regulation] = {
                "text": clean_whitespace(text),
                "description": clean_whitespace(description),
            }

    paras = html.find_all("p")
    content = dict()
    regulation = None
    description = None
    text = None
    for para in paras:
        if "class" not in para.attrs:
            continue
        if para["class"][0] == "vacno0":
            _add_reg_text(regulation, description, text)
            regulation, description = tuple(para.text.split(".")[:2])
            text = str()
        elif para["class"][0] == "sectind0":
            # Remove strikethrough text
            for strikethrough in para.find_all("s"):
                strikethrough.decompose()
            text += f"{para.text} "
    _add_reg_text(regulation, description, text)
    return content


def _get_issue_data(html):
    """Pulls the issue metadata from the header

    Parameters:
    -----------
    html : bs4.BeautifulSoup
        The bs4 reprsentation of the page

    Returns:
    --------
    issue : str
        The issue number
    volume : str
        The volume number
    date : str
        The date of publication
    """
    issue_desc = html.find("div", class_="currentIssue-DateIssue").text

    start, end = re.search(r"(?<=Vol. )\d{2,3}", issue_desc).span()
    volume = issue_desc[start:end]

    start, end = re.search(r"(?<=Iss. )\d{2,3}", issue_desc).span()
    issue = issue_desc[start:end]

    start, end = re.search(r"(?<= - )(.*)", issue_desc).span()
    date = issue_desc[start:end]

    return issue, volume, date


def _get_target_metadata(metadata, target):
    """Finds the metadata for the associated paragraph.

    Parameters
    ----------
    metadata : bs4.BeautifulSoup
        The bs4 representaiton of the metadata section
    target : str
        The name of the metadata tag to search for

    Returns
    -------
    output : str
        The associated metadata
    """
    extraction = None
    for line in metadata:
        if target in line.text:
            return clean_whitespace(line.text.split(":")[1])


def _get_summary(html, summary_class="summary"):
    """Pulls the summary of the regulation from the page

    Parameters
    ----------
    metadata : bs4.BeautifulSoup
        A bs4 representation of the metadata section

    Returns
    -------
    summary : str
        The text summary of the regulation
    """
    paras = html.find_all("p")
    for i, para in enumerate(paras):
        class_ = para.get("class")
        if not class_:
            continue
        if class_[0] == summary_class and i < len(paras) - 1:
            next_para = paras[i + 1]
            return clean_whitespace(next_para.text)


def _get_titles(metadata):
    """Pulls the title and description for the regulations on the page.

    Parameters
    ----------
    metadata : bs4.BeautfiulSoup
        A bs4 representation of the metadata section

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
