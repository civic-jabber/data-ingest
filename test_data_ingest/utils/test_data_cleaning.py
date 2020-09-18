import datetime

import data_ingest.utils.data_cleaning as clean


def test_extract_date():
    assert clean.extract_date("August 1, 2020.") == datetime.datetime(2020, 8, 1)
