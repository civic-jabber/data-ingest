from dataclasses import dataclass
import json


@dataclass
class DataModel:
    @classmethod
    def from_dict(cls, data):
        """Loads the DataModel object from a dictionary containing the field names."""
        return cls(**data)

    def to_dict(self):
        """Converts the DataModel to a dictionary."""
        return vars(self)

    def to_json(self, filename):
        """Serializes the DataModel as JSON."""
        data = self.to_dict()
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    def to_xml(self):
        raise NotImplementedError
