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

The package uses `pip-compiel` to lock dependencies. If you need to add a new
dependency, simply update the appropriate `.in` file in the `requirements` folder and
then run `make pip-compile`.

## Sources

1. OpenStates - data on legislators and the status of legislation
