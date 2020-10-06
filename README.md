# Data Ingest

Welcome to data ingest! This repository contains utilities for ingesting

## Installation

The easiest way to install the package is from the `Makefile`. You can use the following
command.

```
make pip-install
```


### Adding dependencies

The package uses `pip-compile` to lock dependencies. If you need to add a new
dependency, simply update the appropriate `.in` file in the `requirements` folder and
then run `make pip-compile`.

### Non-Python Dependencies

There are also a few Debian packages that are worth installing. For webscraping,
install the Python LXML parser using the following command:

```
apt-get install python-lxml libxml2-dev libxslt-dev
```

The following packages are required for `newspaper` to recognize `.jpg` images
```
apt-get install libjpeg-dev zlib1g-dev libpng-dev
```

To download the corpora that `newspaper` uses for NLP, run the following:
```
curl https://raw.githubusercontent.com/codelucas/newspaper/master/download_corpora.py |
python
```

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

## Usage

### CLI

IF you are running ingest jobs locally, the easiest way to kick them off is via the API.
You can load all of the current ingest jobs using the following CLI command:

```
data_ingest run-ingest
```

## Sources

1. [OpenStates](https://openstates.org) - data on legislators and the status of legislation. To use the Open States API, you'll need to request an API key from the site and create an environment variable called `OPEN_STATES_API_KEY`.
2. [Newspaper](https://newspaper.readthedocs.io) - A Python package for scraping news
   articles.

