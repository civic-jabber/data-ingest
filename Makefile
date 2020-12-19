#######################
# Linting and Testing
#######################

lint:
	make lint-black
	flake8

lint-black:
	black civic_jabber_ingest --check
	black test_civic_jabber_ingest --check
	black dags --check

tidy:
	black civic_jabber_ingest
	black test_civic_jabber_ingest
	black dags

test:
	pytest test_civic_jabber_ingest --cov=civic_jabber_ingest -vv -m "not slow"
	python dags/states.py # Checks to make sure the DAG is valid

################
# Install
################

pip-compile:
	pip-compile requirements/base.in
	pip-compile requirements/dev.in
	pip-compile requirements/test.in

pip-install:
	pip install -r requirements/base.txt
	pip install -r requirements/dev.txt
	pip install -r requirements/test.txt
	pip install -e .

################
# Publish
################

package:
	rm -rf dist/*
	python3 setup.py sdist
	python3 setup.py bdist_wheel

publish:
	make package
	twine upload dist/*

################
# Database
################

db-init:
	psql -U $(user) -d $(db) -h $(host) -f sql/schema.sql
	for file in sql/tables/* ; do \
		psql -U $(user) -d $(db) -h $(host) -f $${file} ; \
	done
