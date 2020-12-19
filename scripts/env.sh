#!/bin/bash

# Get the full real path to the scripts directory and the project directory
full_path="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/$(basename "${BASH_SOURCE[0]}")"
script_path=$(dirname "$full_path")
project_path=$(dirname "$script_path")

# Airflow
export AIRFLOW__CORE__DAGS_FOLDER=${project_path}/dags
export AIRFLOW__LOGGING__LOGGING_LEVEL=WARN
export AIRFLOW__CORE__LOAD_EXAMPLES=False
