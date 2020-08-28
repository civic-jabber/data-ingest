from dataclasses import dataclass
import json

from data_ingest.models.base import DataModel


@dataclass
class MockDataModel(DataModel):
    first_name: str
    last_name: str


def test_data_model_loads_from_dict():
    data = {"first_name": "Matt", "last_name": "Robinson"}
    data_model = MockDataModel.from_dict(data)
    assert (data_model.first_name, data_model.last_name) == ("Matt", "Robinson")


def test_date_model_serializes_to_json(tmpdir):
    filename = f"{tmpdir.dirname}/mock_output.json"
    data = {"first_name": "Matt", "last_name": "Robinson"}
    data_model = MockDataModel.from_dict(data)
    data_model.to_json(filename)

    with open(filename, "r") as f:
        data_json = json.load(f)
    assert data_json == data_model.to_dict()
