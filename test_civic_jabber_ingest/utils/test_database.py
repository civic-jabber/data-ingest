import unittest

from dataclasses import dataclass
import pandas as pd
import psycopg2
import testing.postgresql

import civic_jabber_ingest.utils.database as database
from civic_jabber_ingest.utils.environ import modified_environ


def test_connect(monkeypatch):
    monkeypatch.setattr(psycopg2, "connect", lambda connection_str: connection_str)
    env = {"CIVIC_JABBER_PG_USER": "tiki", "CIVIC_JABBER_PG_HOST": "localhost"}
    with modified_environ(**env):
        conn = database.connect()
        assert conn == "dbname=postgres user=tiki host=localhost port=5432"


def handler(postgresql):
    conn = psycopg2.connect(**postgresql.dsn())
    with conn.cursor() as cursor:
        cursor.execute("CREATE SCHEMA IF NOT EXISTS fakeroo")
        cursor.execute("CREATE TABLE IF NOT EXISTS fakeroo.parrot(id text, color text)")
    conn.commit()


Postgresql = testing.postgresql.PostgresqlFactory(
    cache_initialized_db=True, on_initialized=handler
)


@dataclass
class Parrot:
    id: str = "1"
    color: str = "blue"


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.postgresql = Postgresql()

    def tearDown(self):
        self.postgresql.stop()

    def test_insert(self):
        conn = psycopg2.connect(**self.postgresql.dsn())
        parrot = Parrot()

        database.execute_sql("TRUNCATE fakeroo.parrot", connection=conn)

        database.insert_obj(parrot, schema="fakeroo", table="parrot", connection=conn)
        data = pd.read_sql("SELECT * FROM fakeroo.parrot", conn)
        pd.testing.assert_frame_equal(
            data, pd.DataFrame({"id": ["1"], "color": ["blue"]})
        )

        database.delete_by_id("1", schema="fakeroo", table="parrot", connection=conn)
        data = pd.read_sql("SELECT * FROM fakeroo.parrot", conn)
        assert len(data) == 0


def test_news_source_top_keyworkds(monkeypatch):
    mock_keywords = [(435, "state"), (423, "county")]

    def mock_execute_sql(*args, **kwargs):
        return mock_keywords

    monkeypatch.setattr(database, "execute_sql", mock_execute_sql)
    assert database.news_source_top_keywords(None) == mock_keywords
