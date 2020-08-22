import pytest

from data_ingest.models.regulation import Regulation


NOT_IMPLEMENTED_METHODS = [
    "get_title",
    "get_description",
    "get_text",
    "get_summary",
    "get_effective_date",
    "get_point_of_contact",
    "get_volume",
    "get_issue",
    "get_date",
    "get_authority",
]


def test_regulation_id():
    regulation = Regulation()
    assert isinstance(regulation.get_id(), str)


@pytest.mark.parametrize("method_name", NOT_IMPLEMENTED_METHODS)
def test_stub_methods_raise_not_implemented_error(method_name):
    regulation = Regulation()
    with pytest.raises(NotImplementedError):
        method = getattr(regulation, method_name)
        method()
