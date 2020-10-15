from copy import deepcopy

import newspaper
import tqdm

from data_ingest.models.article import Article
import data_ingest.utils.database as db
from data_ingest.utils.config import read_config


_connection = None


def _connect():
    global _connection
    if not _connection or _connection.closed > 0:
        _connection = db.connect()


def load_news():
    _connect()
    newspaper_config = read_config("newspaper")
    for paper_name, metadata in tqdm.tqdm(newspaper_config.items()):
        paper = newspaper.build(metadata["url"])
        paper_data = {
            "source_id": metadata["id"],
            "source_name": paper_name,
            "source_brand": paper.brand,
            "source_description": paper.description,
        }

        for paper_article in paper.articles:
            try:
                paper_article.build()
            except newspaper.ArticleException:
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
