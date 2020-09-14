#######################
# Linting and Testing
#######################

lint:
	black data_ingest --check

lint-black:
	black data_ingest --check
	black test_data_ingest --check

tidy:
	black data_ingest
	black test_data_ingest

test:
	pytest test_data_ingest --cov=data_ingest -vv

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
# Database
################

db-init:
	psql -U $(user) -d $(db) -f sql/schema.sql
	for file in sql/tables/* ; do \
		psql -U $(user) -d $(db) -f $${file} ; \
	done
