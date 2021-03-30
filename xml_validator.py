import logging

from os import access, R_OK
from lxml import etree


class XMLValidator:
    """
    Validates XML files using the provided XSD schema.

    Parameters
    ----------
    xsd_path : str
        Path to the file containing the XSD schema.
    valid_dtd : Optional[bool
        Also validate the DTD (default) or not.
    """

    def __init__(self, xsd_path, valid_dtd=True, large_file=False):
        self._logger = logging.getLogger(__name__)

        self._valid_dtd = valid_dtd
        self._large_file = large_file

        self._schema = self._read_xsd(xsd_path)

    def validate(self, xml_paths):
        """
        Validate a set of XML files using the provided schema.

        Parameters
        ----------
        xml_paths : List[str]
            List of file paths to validate.
        """

        # TODO: parallelize with joblib if needed
        for xml_path in xml_paths:
            if not self._is_readable(xml_path):
                # Log warning but continue with the remaining files
                self._logger.warning(f"Cannot read from XML file: {xml_path}")
                continue

            self._logger.info(f"PROCESSING:   [{xml_path}]")
            parser = etree.XMLParser(huge_tree=self._large_file)
            xml_doc = etree.parse(xml_path, parser=parser)

            if self._schema.validate(xml_doc):
                self._logger.info(f"SUCCESS:      [{xml_path}] Validation was succesful!")
            else:
                for error in self._schema.error_log:
                    self._logger.error(f"ERROR:        [{xml_path} - L:{error.line}] - {error.message}")

            self._logger.info(f"FINISHED:     [{xml_path}]")


    def _read_xsd(self, xsd_path):
        """Reads and parses an XSD schema from the provided file path.

        Parameters
        ----------
        xsd_path : str
            Path to the XSD schema file.

        Returns
        -------
        lxml.etree.XMLSchema
            Parsed XML tree of the XSD schema.
        """

        if not self._is_readable(xsd_path):
            raise RuntimeError("Cannot read from XSD file path.")

        with open(xsd_path, "r") as xsd_file:
            return etree.XMLSchema(file=xsd_file)

    def _is_readable(self, file_path):
        """
        Checks whether a file is readable or not.

        Parameters
        ----------
        file_path : str
            Path to the file to check.

        Returns
        -------
        bool
            Boolean indicating whether the file is readable.
        """

        readable = access(file_path, R_OK)

        if not readable:
            self._logger.warning(f"Could not read file: {file_path}")

        return readable
