import datetime

import data_ingest.utils.data_cleaning as clean


def test_extract_date():
    assert clean.extract_date("August 1, 2020") == datetime.datetime(2020, 8, 1)


def test_extract_date_works_with_period():
    assert clean.extract_date("August 1, 2020.") == datetime.datetime(2020, 8, 1)


def test_extract_date_returns_none_with_non_string():
    assert clean.extract_date(2020) is None


def test_clean_whitespace():
    clean.clean_whitespace("  parrots  ") == "parrots"


def test_extract_phone_number():
    example = "Jenn Walker, 215-867-5309, jenn@walker.com"
    assert clean.extract_phone_number(example) == "215-867-5309"


def test_extract_email():
    example = "Jenn Walker, 215-867-5309, jenn@walker.com"
    assert clean.extract_email(example) == "jenn@walker.com"
