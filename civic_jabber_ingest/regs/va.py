import os
import re
from time import sleep

import civic_jabber_ingest.external_services.aws as aws
from civic_jabber_ingest.models.contact import Contact
from civic_jabber_ingest.models.regulation import Regulation
from civic_jabber_ingest.models.title import Title
import civic_jabber_ingest.utils.database as database
from civic_jabber_ingest.utils.data_cleaning import (
    clean_whitespace,
    extract_date,
    extract_email,
    extract_phone_number,
)
from civic_jabber_ingest.utils.logging import get_logger, tqdm
import civic_jabber_ingest.utils.config as config
from civic_jabber_ingest.utils.scrape import get_page


LOGGER = get_logger()


VA_REGISTRY_PAGE = "http://register.dls.virginia.gov/archive.aspx"
VA_REG_TEMPLATE = "http://register.dls.virginia.gov/toc.aspx?voliss={vol}:{issue}"
VA_REGULATION = "http://register.dls.virginia.gov/details.aspx?id={site_id}"


SUB_DIRECTORY_RE = re.compile(r"\S*/va/\d{1,2}$")
S3_PREFIX_RE = re.compile(r"\d{2}\/\d{2}")


def _get_va_regulation_dir():
    va_dir = os.path.join(config.local_regs_directory(), "va")
    if not os.path.exists(va_dir):
        os.mkdir(va_dir)
    return va_dir


def load_va_regulations(sleep_time=1, source="postgres", dev=False):
    """Downloads and stores VA regulations locally as XML files.

    Parameters
    ----------
    sleep_time : int
        The amount of time to sleep between calls to the registry website
    local : bool
        If True, checks the local directory for loaded issues. Otherwise, checks S3
    dev : bool
        If True, uses the dev S3 bucket
    """
    connection = database.connect() if source == "postgres" else None
    registry_issues = list_all_volumes()
    loaded_issues = _get_loaded_issues(source=source, dev=dev, connection=connection)
    issues_to_process = registry_issues.difference(loaded_issues)

    for volume, issue in issues_to_process:
        LOGGER.info(f"Loading regulations for Vol. {volume} Issue {issue}.")

        volume_dir = os.path.join(_get_va_regulation_dir(), volume)
        if not os.path.exists(volume_dir):
            os.mkdir(volume_dir)

        issue_dir = os.path.join(volume_dir, issue)
        if not os.path.exists(issue_dir):
            os.mkdir(issue_dir)

        issue_ids = get_issue_ids(volume, issue)
        for issue_id in tqdm(issue_ids):
            filename = os.path.join(issue_dir, f"{issue_id}.xml")
            reg = get_regulation(issue_id)
            if source == "postgres":
                titles = reg_to_titles(reg)
                for title in titles:
                    database.insert_obj(title, "titles", connection=connection)
            else:
                regulation = normalize_regulation(reg)
                regulation.to_xml(filename)
            sleep(sleep_time)

    if source == "aws":
        aws.sync_state("va")


def _get_loaded_issues(directory=None, source="postgres", dev=False, connection=None):
    """Pulls a list of issues and volumes that have already been loaded in the local
    filesystem

    Parameters
    ----------
    directory : str
        The directory to check for loaded issues.
    source : str
        Where to look for the loaded issues
    dev : bool
        If True, uses the dev S3 bucket
    connection : psycopg2.Connection
        The database connection, if applicable

    Returns
    -------
    issues : set
        A set of tuples where the first element is the volume and the second element is
        the issue
    """
    directory = _get_va_regulation_dir() if not directory else directory
    loaded_issues = set()
    if source == "local":
        for directory, subdirectories, _ in os.walk(directory):
            # Look for directories that look like ../va/1, not ../va or ../va/1/2
            if SUB_DIRECTORY_RE.search(directory) is not None:
                volume = directory.split("/")[-1]
                for issue in subdirectories:
                    loaded_issues.add((volume, issue))
    elif source == "aws":
        files = aws.s3_ls(prefix="va", dev=dev)
        for filename in files:
            result = S3_PREFIX_RE.search(filename)
            if result:
                volume, issue = tuple(result.group().split("/"))
                loaded_issues.add((volume, issue))
    elif source == "postgres":
        sql = """
            SELECT DISTINCT volume, issue
            FROM civic_jabber.titles
        """
        connection = database.connect() if not connection else connection
        loaded_issues = set(database.execute_sql(sql, connection, select=True))
    else:
        raise ValueError("Invalid option for searching loaded issues.")

    return loaded_issues


def get_regulation(site_id):
    """Pulls the html for a regulation using the site id. Note, in some cases there are
    multiple regulations addressed on a single page.

    Parameters
    ----------
    site_id : str
        The site id for the page

    Returns
    -------
    regulation : dict
        A dictionary representing the infromation scraped from the registry site.
    """
    url = VA_REGULATION.format(site_id=site_id)
    html = get_page(url)
    regulation = _parse_html(html)
    regulation["state"] = "va"
    regulation["link"] = url
    return regulation


def normalize_regulation(regulation):
    """Normalizes the regulation dictionary and converts it to the standardized
    Regulation object.

    Parameters
    ----------
    regulation : dict
        A dictionary representing the infromation scraped from the registry site.

    Returns:
    --------
    normalized_regulation : Regulation
        A base Regulation object
    """
    normalized_reg = dict()

    body = str()
    for subtitle, content in regulation["content"].items():
        body += f"{subtitle}. {content['description']}\n{content['text']}\n"
    normalized_reg["body"] = body if body else None

    contact = regulation.get("contact", None)
    if contact:
        first_name, last_name, email, phone = _parse_contact(contact)
        contact = Contact.from_dict(
            {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone": phone,
            }
        )
        normalized_reg["contacts"] = [contact]

    date = regulation["date"]
    if "through" in date:
        start_date, end_date = tuple(date.split("through")[:2])
        normalized_reg["start_date"] = extract_date(start_date)
        normalized_reg["end_date"] = extract_date(end_date)
        del regulation["date"]
    else:
        normalized_reg["date"] = extract_date(date)
    normalized_reg["register_date"] = extract_date(regulation["register_date"])

    for key in vars(Regulation()):
        if key not in normalized_reg and key in regulation:
            normalized_reg[key] = regulation[key]

    return Regulation.from_dict(normalized_reg)


def reg_to_titles(regulation):
    """Normalizes the regulation dictionary and converts it to the standardized
    Title object.

    Parameters
    ----------
    regulation : dict
        A dictionary representing the infromation scraped from the registry site.

    Returns:
    --------
    normalized_title : Title
        A base Title object
    """
    titles = list()

    summary = regulation.get("summary")
    if not summary:
        summary = regulation.get("preamble")

    for sub_title in regulation["titles"]:
        title = dict()

        title["title"] = sub_title["code"]
        title["description"] = sub_title["description"]

        date = regulation["date"]
        if date:
            if "through" in date:
                start_date, end_date = tuple(date.split("through")[:2])
                title["start_date"] = extract_date(start_date)
                title["end_date"] = extract_date(end_date.replace("  ", " "))
            else:
                title["date"] = extract_date(date)
        title["register_date"] = extract_date(regulation["register_date"])

        for key in vars(Title()):
            if key not in title and key in regulation and key != "date":
                title[key] = regulation[key]

        titles.append(Title.from_dict(title))

    return titles


def list_all_volumes():
    """Lists all available issues and volumes from the VA registry webpage. Only returns
    volumes that are available on HTML.

    Returns
    -------
    volumes : dict
        A dictionary where the volumes are the keys and the issues are list entries.
    """
    volumes = set()
    html = get_page(VA_REGISTRY_PAGE)
    details = html.find_all(class_="archiveDetail")
    for line in details:
        links = line.find_all("a")
        for link in links:
            if link.text != "PDF":
                volume, issue = tuple(link["href"].split("=")[-1].split(":"))
                volumes.add((volume, issue))
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

    reg["issue"] = issue.zfill(2)
    reg["volume"] = volume.zfill(2)

    reg["notice"] = _get_notice(html)
    reg["content"] = _get_regulation_content(html)
    reg["summary"] = _get_summary(html)
    reg["preamble"] = _get_summary(html, summary_class="preamble")

    reg["status"] = _get_title_info(html, "Status")
    reg["title"] = _get_title_info(html, "Title")
    reg["chapter"] = _get_title_info(html, "Chapter")
    reg["chapter_description"] = _get_title_info(html, "Description")

    reg["titles"] = _get_titles(metadata)
    reg["authority"] = _get_target_metadata(metadata, "Authority")
    reg["contact"] = _get_target_metadata(metadata, "Contact")

    reg["register_date"] = date
    reg["date"] = _get_target_metadata(metadata, "Date")
    if not reg["date"]:
        reg["date"] = _get_target_metadata(metadata, "Deadline")
    return reg


def _get_title_info(html, key):
    """Pulls title information for the regulation.

    Parameters
    ----------
    html : bs4.BeautifulSoupt
        The bs4 representation of the site
    key : str
        The last element of the class name for the div to target

    Returns
    -------
    title_info : str
        The relevant title information
    """
    div = html.find("div", {"id": f"ContentPlaceHolder1_div{key}"})
    return div.text if div else None


def _get_notice(html):
    """Pulls title information for the regulation.

    Parameters
    ----------
    html : bs4.BeautifulSoupt
        The bs4 representation of the site

    Returns
    -------
    notice : str
        The string of the notice
    """
    para = html.find("p", class_="notice0")
    return para.decode_contents() if para else None


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
                "description": clean_whitespace(text),
                "code": clean_whitespace(description),
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
            if "." in para.text:
                regulation, description = tuple(para.text.split(".")[:2])
            text = str()
        elif para["class"][0] == "sectind0":
            if not text:
                text = str()
            text += f"{para.decode_contents()} "
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

    start, end = re.search(r"(?<=Vol. )\d{1,3}", issue_desc).span()
    volume = issue_desc[start:end]

    start, end = re.search(r"(?<=Iss. )\d{1,3}", issue_desc).span()
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
    for line in metadata:
        if target in line.text:
            if target == "Date" and target.endswith("."):
                line = line[:-1]
            if ":" in line.text:
                return clean_whitespace(line.text.split(":")[1])
            else:
                return None


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
        if "Date" in line.text:
            break
        bold = line.find_all("b") + line.find_all("strong")
        text = str()
        for item in bold:
            text += item.text
        if text:
            if "." in text:
                title, description = tuple(text.split(".")[:2])
                titles.append(
                    {
                        "code": clean_whitespace(title),
                        "description": clean_whitespace(description),
                    }
                )
    return titles


def _parse_contact(contact):
    """Extracts pertinent information from the contact string

    Parameters
    ----------
    contact : str
        A string with contact information

    Returns
    -------
    first_name : str
    last_name : str
    email : str
    phone_number : str
    """
    # Assumes name appears first in the list
    first_name, last_name = None, None
    name = contact.split(",")[0]
    if len(name.split()) > 1:
        first_name = name.split()[0]
        last_name = " ".join(name.split()[1:])

    email = extract_email(contact)
    phone_number = extract_phone_number(contact)

    return first_name, last_name, email, phone_number
