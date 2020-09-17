# Data Ingest

Welcome to data ingest! This repository contains utilities for ingesting

## Installation

The easiest way to install the package is from the `Makefile`. You can use the following
command.

```
make pip-install
```

There are also a few Debian packages that are worth installing. For webscraping,
install the Python LXML parser using the following command:

```
apt-get install python-lxml
```

### Adding dependencies

The package uses `pip-compile` to lock dependencies. If you need to add a new
dependency, simply update the appropriate `.in` file in the `requirements` folder and
then run `make pip-compile`.

## Database

### Initializing the Database

The scripts for setting of the schema and tables are the in the `sql` folder. You can
initialize the database using the following command:

```
make db-init user={user} db={database} host={host}
```

The command will loop through the SQL files in the `sql/tables` folder.

### Connections

The database connections utility manages connections to the database. To connect to a
specific database, set the following environmental variable:

```
CIVIC_JABBER_PG_HOST
CIVIC_JABBER_PG_PORT
CIVIC_JABBER_PG_DB
CIVIC_JABBER_PG_USER
```

If you do not set an environmental variable, it will assume a default value. You can
connect to the database with:

```python
from data_ingest.utils.connection import connect

connection = connect()

```

## Sources

1. OpenStates - data on legislators and the status of legislation
