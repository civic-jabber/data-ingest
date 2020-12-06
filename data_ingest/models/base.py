from dataclasses import dataclass
import json

from bs4 import BeautifulSoup


@dataclass
class DataModel:
    @classmethod
    def from_dict(cls, data):
        """Loads the DataModel object from a dictionary containing the field names."""
        return cls(**data)

    def to_dict(self, drop_empty=False):
        """Converts the DataModel to a dictionary.

        Parameters
        ----------
        drop_empty : bool
            If True, omits top levels keys that are None

        Returns
        -------
        data : dict
            A dictionary representation of the odel

        """
        data = vars(self)
        if drop_empty:
            keys = list(data.keys())
            for key in keys:
                if data[key] is None:
                    del data[key]
        return data

    def to_json(self, filename):
        """Serializes the DataModel as JSON.

        Parameters
        ----------
        filename : str
            The filename for the serialized JSON output.
        """
        data = self.to_dict()
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    def to_xml(self, filename):
        """Serializes the DataModel as XML

        Parameters
        ----------
        filename : str
            The filename for the serialized JSON output.
        """
        xml = self.xml_template()
        if xml:
            # We use the bs4 parser to prettify the XML prior to writing
            xml = BeautifulSoup(self.xml_template(), "xml")
            with open(filename, "w") as f:
                f.write(xml.prettify())

    def xml_template(self):
        """Converts the data object to XML. The XML templates are in the schemas
        directory.

        Returns
        -------
        xml : str
            An XML representation of the data object

        """
        raise NotImplementedError
