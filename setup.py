from setuptools import setup, find_packages

from civic_jabber_ingest.__version__ import __version__


requirements = 'requirements/base.txt'
install_requires = []
with open(requirements) as f:
    install_requires = f.read().splitlines()

setup(
    name="civic_jabber_ingest",
    description="Utilities for ingesting legislative data",
    author="Civic Jabber",
    author_email="matt@civicjabber.com",
    packages=find_packages(),
    version=__version__,
    entry_points={"console_scripts": "civic_jabber_ingest=civic_jabber_ingest.cli:main"},
    install_requires=install_requires,
    package_data={
        "civic_jabber_ingest.config": ["*.yml"],
        "civic_jabber_ingest.schemas": ["*.xml", "*.xsd"],
    }
)
