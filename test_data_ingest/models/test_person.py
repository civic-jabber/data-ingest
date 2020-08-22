import pytest

from data_ingest.models.person import Person, Address


PERSON_METHODS = list(Person.__dict__.values())
ADDRESS_METHODS = list(Address.__dict__.values())
ALL_METHODS = PERSON_METHODS + ADDRESS_METHODS


@pytest.mark.parametrize("method", ALL_METHODS)
def test_person(method):
    if method.__class__.__name__ == "function":
        with pytest.raises(NotImplementedError):
            method()
