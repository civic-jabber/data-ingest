import os
import unittest

from dataclasses import dataclass
import pandas as pd
import psycopg2
import testing.postgresql

import data_ingest.utils.connection as connection
from data_ingest.utils.environ import modified_environ


def test_connect(monkeypatch):
    monkeypatch.setattr(psycopg2, "connect", lambda connection_str: connection_str)
    with modified_environ(CIVIC_JABBER_PG_USER="tiki"):
        conn = connection.connect()
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

        connection._execute_sql("TRUNCATE fakeroo.parrot", connection=conn)

        connection.insert_obj(parrot, schema="fakeroo", table="parrot", connection=conn)
        data = pd.read_sql("SELECT * FROM fakeroo.parrot", conn)
        pd.testing.assert_frame_equal(
            data, pd.DataFrame({"id": ["1"], "color": ["blue"]})
        )

        connection.delete_by_id("1", schema="fakeroo", table="parrot", connection=conn)
        data = pd.read_sql("SELECT * FROM fakeroo.parrot", conn)
        assert len(data) == 0
