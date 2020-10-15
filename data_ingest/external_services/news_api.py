import os
import re
import urllib

from requests import Session
import tqdm

from data_ingest.utils.config import read_config


class NewsAPISession(Session):
    """Base class for making API calls from the News API."""

    base_url = "https://newsapi.org/v2/"

    def __init__(self, api_key=None):
        super().__init__()

        api_key = api_key if api_key else os.environ.get("NEWS_API_KEY")
        if not api_key:
            raise ValueError(
                "The API key must be specified in the api_key argument or "
                "using the NEWS_API_KEY environment variable. "
            )
        self.api_key = api_key

    def __str__(self):
        return self.__class__.__name__

    def request(self, method, url, *args, **kwargs):
        params = kwargs.get("params", dict())
        params.update({"apiKey": self.api_key})
        kwargs["params"] = params

        url = self._create_url(url)
        return super().request(method, url, *args, **kwargs)

    def _create_url(self, url):
        if not self.base_url:
            raise ValueError("Base URL for the external service has not been set.")
        return f"{self.base_url}{url}"


def get_domains():
    domains = set()
    papers = read_config("newspaper")
    for paper in papers.values():
        domain = paper["url"].split("//")[1].split("/")[0]
        domain = domain.replace("www.", "")
        domains.add(domain)
    return domains
