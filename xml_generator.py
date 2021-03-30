import uuid
import datetime as dt

import numpy as np
import pandas as pd

from jinja2 import Template


class XMLGenerator:
    """Dummy data XML file generator."""

    _template_file = "generator/xml_generator.tmpl"

    def __init__(self, xml_path, nrecords=100, date=None):
        self._xml_path = xml_path
        self._nrecords = int(nrecords)
        self._date = date or dt.date.today()

        self._template = Template(self._load_template())

    def _load_template(self):
        """Loads the Jinja2 template from file."""
        with open(self._template_file, "r") as tmpl_file:
            return tmpl_file.read()

    def _gen_records(self):
        """Creates the dummy data as pandas DataFrame."""

        # Create fixed set of UUID to sample for speed
        # Note: Duplicates will occur, but for demo data that's OK.
        uuids = [str(uuid.uuid4()) for _ in range(self._nrecords // 2)]

        times = [
            dt.datetime.combine(self._date, dt.time(h, m, s)).strftime(
                "%Y-%m-%dT%H:%M:%S"
            )
            for h, m, s in zip(
                np.random.randint(0, 24, self._nrecords),
                np.random.randint(0, 60, self._nrecords),
                np.random.randint(0, 60, self._nrecords),
            )
        ]

        return pd.DataFrame(
            {
                "datetime": times,
                "product": np.random.choice(uuids, self._nrecords, replace=True),
                "seller": np.random.choice(uuids, self._nrecords, replace=True),
                "buyer": np.random.choice(uuids, self._nrecords, replace=True),
                "price": np.random.normal(100, 20, self._nrecords),
                "quantity": np.random.random_integers(1, 100, self._nrecords),
            }
        ).sort_values("datetime").to_dict("records")

    def generate(self):
        """Generates an XML file with dummy data."""

        data = {
            "current_date": self._date.strftime("%Y-%m-%d"),
            "n_records": self._nrecords,
            "records": self._gen_records(),
        }

        with open(self._xml_path, "w") as out_file:
            out_file.write(self._template.render(**data))

