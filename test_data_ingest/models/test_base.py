from dataclasses import dataclass
import json

import pytest

from data_ingest.models.base import DataModel
from data_ingest.utils.xml import get_jinja_template


@dataclass
class MockDataModelBase(DataModel):
    first_name: str
    last_name: str


@dataclass
class MockDataModel(MockDataModelBase):
    def xml_template(self):
        data = self.to_dict()
        template = get_jinja_template("contact")
        return template.render(data=data)


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


def test_date_model_serializes_to_xml(tmpdir):
    filename = f"{tmpdir.dirname}/mock_output.xml"
    data = {"first_name": "Matt", "last_name": "Robinson"}
    data_model = MockDataModel.from_dict(data)
    data_model.to_xml(filename)

    with open(filename, "r") as f:
        xml = f.read()
    assert xml == data_model.xml_template()


def test_base_raises_with_no_xml_method():
    data = {"first_name": "Matt", "last_name": "Robinson"}
    data_model = MockDataModelBase.from_dict(data)
    with pytest.raises(NotImplementedError):
        data_model.xml_template()
