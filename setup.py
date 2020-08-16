from setuptools import setup, find_packages

from data_ingest.__version__ import __version__

setup(
    name="data_ingest",
    description="Utilities for ingesting legislative data",
    author="Civic Jabber",
    author_email="matt@civicjabber.com",
    packages=find_packages(),
    version=__version__,
    entry_points={"console_scripts": "data_ingest=data_ingest.cli:main"},
)
