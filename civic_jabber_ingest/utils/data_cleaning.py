import datetime
import re


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
    if not isinstance(text, str):
        return None
    return re.sub(r"\s", " ", text.strip())


MONTH_DAY_YEAR_RE = re.compile(r"[A-Z][a-z]+ \d{1,2}, \d{4}")


def extract_date(text):
    """Converts a text string with a date to a datetime object

    Parameters
    ----------
    text : str
        The text to clean

    Returns
    -------
    date : datetime.datetime
        A datetime object
    """
    if not isinstance(text, str):
        return None

    if MONTH_DAY_YEAR_RE.search(text):
        start, end = MONTH_DAY_YEAR_RE.search(text).span()
        return datetime.datetime.strptime(text[start:end], "%B %d, %Y")


EMAIL_RE = re.compile(r"[a-zA-Z]*@[a-z]*\.(com|gov)")


def extract_email(text):
    """Extracts an email from a string

    Parameters
    ----------
    text : str
        The text to clean

    Returns
    -------
    email : str
        The email
    """
    if not isinstance(text, str):
        return None

    if EMAIL_RE.search(text):
        start, end = EMAIL_RE.search(text).span()
        return text[start:end]


PHONE_NUMBER_RE = re.compile(r"\d{3}-\d{3}-\d{4}")


def extract_phone_number(text):
    """Extracts an phone number from a string

    Parameters
    ----------
    text : str
        The text to clean

    Returns
    -------
    phone_number : str
        The phone number
    """
    if not isinstance(text, str):
        return None

    if PHONE_NUMBER_RE.search(text):
        start, end = PHONE_NUMBER_RE.search(text).span()
        return text[start:end]
