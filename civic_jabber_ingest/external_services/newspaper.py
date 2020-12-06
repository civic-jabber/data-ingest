from copy import deepcopy
import time
import uuid

import newspaper
import tqdm

from civic_jabber_ingest.models.article import Article
import civic_jabber_ingest.utils.database as db
from civic_jabber_ingest.utils.config import read_config
from civic_jabber_ingest.utils.scrape import get_page


_connection = None


def _connect():
    global _connection
    if not _connection or _connection.closed > 0:
        _connection = db.connect()


def load_news(states=None):
    """Scrapes newspaper articles from all of the sources listed in the newspaper config
    file and loads the results into the database.

    Parameters
    ----------
    states : list
        A list of states to include in the scraping job. If blank, the function will
        scrape all states
    """
    _connect()
    print("Reading newspaper configuration file ...")
    valid_papers = read_config("newspaper")
    if states:
        states = [states] if isinstance(states, str) else states
        valid_papers = [
            paper for paper in valid_papers if _check_state(states, paper["states"])
        ]

    for metadata in tqdm.tqdm(valid_papers):
        paper = newspaper.build(metadata["url"])
        paper_data = {
            "source_id": metadata["id"],
            "source_name": metadata["name"],
            "source_brand": paper.brand,
            "source_description": paper.description,
        }

        for paper_article in paper.articles:
            try:
                paper_article.build()
            except (newspaper.ArticleException, ValueError):
                continue

            if not paper_article.summary:
                continue

            article_data = deepcopy(paper_data)
            article_data.update(
                {
                    "title": paper_article.title,
                    "body": paper_article.text,
                    "summary": paper_article.summary,
                    "keywords": paper_article.keywords,
                    "images": list(paper_article.images),
                    "url": paper_article.url,
                }
            )
            article = Article.from_dict(article_data)
            db.insert_obj(article, table="articles", connection=_connection)


def _check_state(enabled_states, paper_states):
    """Checks to see if the newspaper object contains a state that we want to scrape.

    Parameters
    ----------
    enabled_states : list
        The states that we want to scrape
    paper_states : list
        The states that are applicable to the newspaper

    Returns
    -------
    valid : bool
        True if the paper meets the criteria for the scraping job
    """
    enabled_states = set(enabled_states)
    paper_states = set(paper_states)
    return bool(enabled_states.intersection(paper_states))


USNPL_URL = "https://www.usnpl.com"


def find_sources(sleep_time=1):
    """Scrapes the US Newspaper Listing websites to find URLs for local newspapers in
    all 50 US states.

    Parameters
    ----------
    sleep_time : int
        The amount of time to sleep in between states

    Returns
    -------
    sources : list
        A list

    """
    page = get_page(USNPL_URL)
    states = page.find("div", class_="row desktop").find_all("a")

    sources = list()
    for state in tqdm.tqdm(states):
        state_code = state.get("href").split("=")[-1]
        sources.extend(_state_sources(state_code))
        time.sleep(sleep_time)
    return sources


def _state_sources(state_code):
    """Extracts the newspaper listings from the USNPL state page.

    Parameters
    ----------
    state : str
        The two letter state code for the state

    Returns
    -------
    results : list
        A list of sources for the state
    """
    url = f"{USNPL_URL}/search/state?state={state_code}"
    state_page = get_page(url)

    result_table = state_page.find("table", class_="table table-sm")
    result_rows = result_table.find_all("tr")
    results = list()
    for row in result_rows:
        if not row.find_all("td", class_="w-50"):
            continue

        paper_name = row.find("td", class_="w-50").text
        paper_url = row.find("td", class_="w-10").find("a").get("href")

        results.append(
            {
                "id": uuid.uuid4().hex,
                "name": paper_name,
                "url": paper_url,
                "states": [state_code.lower()],
            }
        )
    return results
