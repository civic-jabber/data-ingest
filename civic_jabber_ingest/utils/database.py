import os

import psycopg2


def connect():
    """Connects to the database specified by the environmental variables."""
    host = os.environ.get("CIVIC_JABBER_PG_HOST", "localhost")
    port = os.environ.get("CIVIC_JABBER_PG_PORT", "5432")
    db = os.environ.get("CIVIC_JABBER_PG_DB", "postgres")
    user = os.environ.get("CIVIC_JABBER_PG_USER", "postgres")
    return psycopg2.connect(f"dbname={db} user={user} host={host} port={port}")


def execute_sql(sql, connection, values=None, select=False, commit=True):
    """Executes a SQL statement against the database.

    Parameters
    ----------
    sql : str
        The SQL statement to execute
    connection : psycopg2.connection
        The database connection
    select : bool
        If True, returns the query results as tuples
    commit : bool
        Determines whether or not to commit the database operation upon completion
    """
    if not connection:
        connection = connect()
    with connection.cursor() as cursor:
        cursor.execute(sql, values)
        if select:
            return cursor.fetchall()
    if commit:
        connection.commit()


def insert_obj(obj, table, schema="civic_jabber", connection=None):
    """Inserts a data model object into the specified tabele.

    Parameters
    ----------
    obj : civic_jabber_ingest.models.base.DataModel
        The data object to insert into the database table
    table : str
        The table for the insert
    schema : str
        The schema for the insert
    connection : psycopg2.connection
        The database connection
    """
    columns = ", ".join(vars(obj).keys())
    subs = ", ".join(["%s" for i in range(len(vars(obj)))])
    values = tuple(vars(obj).values())
    sql = f"""
        INSERT INTO {schema}.{table} ({columns})
        VALUES ({subs})
    """
    execute_sql(sql, connection, values)


def delete_by_id(id_, table, schema="civic_jabber", id_col="id", connection=None):
    """Deletes an object from a database table using the id

    Parameters
    ----------
    id_ : str
        The unique id for the object
    table : str
        The table for the insert
    schema : str
        The schema for the insert
    id_col : str
        The id column for the table
    connection : psycopg2.connection
        The database connection
    """
    sql = f"""
        DELETE FROM {schema}.{table}
        WHERE {id_col}='{id_}'
    """
    execute_sql(sql, connection)
