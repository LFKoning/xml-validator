"""Module that runs a demo of the XMLValidatr class."""
import os
import logging

from glob import glob
from validator import XMLValidator


def get_xml_files(xml_path):
    """Grabs all XML files from the input path."""

    return glob(os.path.join(xml_path, "*.xml"))


def main():
    """Runs the XMLValidator on a set of test files."""

    logging.basicConfig(
        level="INFO",
        format="[%(asctime)s] %(levelname)-6s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    files = get_xml_files("data")
    val = XMLValidator("xml_schema.xsd", False)
    val.validate(files)


if __name__ == "__main__":
    main()
