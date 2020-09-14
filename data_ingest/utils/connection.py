import os

import psycopg2


def connect():
    """Connects to the database specified by the environmental variables."""
    host = os.environ.get("CIVIC_JABBER_PG_HOST", "localhost")
    port = os.environ.get("CIVIC_JABBER_PG_PORT", "5432")
    db = os.environ.get("CIVIC_JABBER_PG_DB", "postgres")
    user = os.environ.get("CIVIC_JABBER_PG_USER", "postgres")
    return psycopg2.connect(f"dbname={db} user={user} host={host} port={port}")
