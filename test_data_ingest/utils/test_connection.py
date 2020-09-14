import psycopg2
import os

import data_ingest.utils.connection as connection
from data_ingest.utils.environ import modified_environ


def test_connect(monkeypatch):
    monkeypatch.setattr(psycopg2, "connect", lambda connection_str: connection_str)
    with modified_environ(CIVIC_JABBER_PG_USER="tiki"):
        conn = connection.connect()
        assert conn == "dbname=postgres user=tiki host=localhost port=5432"
