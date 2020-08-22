import pytest

from data_ingest.models.regulation import Regulation


REGULATION_METHODS = Regulation.__dict__.values()


@pytest.mark.parametrize("method", REGULATION_METHODS)
def test_regulation(method):
    if method.__class__.__name__ == "function":
        with pytest.raises(NotImplementedError):
            method()
