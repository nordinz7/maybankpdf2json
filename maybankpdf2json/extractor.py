import io
from typing import List, Optional

from .utils import Output, OutputV2, convert_to_json, convert_to_jsonV2


class MaybankPdf2Json:
    """
    Extracts transaction data from a Maybank PDF statement and converts it to JSON.

    Attributes:
        buffer (io.BufferedReader): The PDF file buffer.
        pwd (str): The password for the PDF file.
    """

    def __init__(self, buffer: io.BufferedReader, pwd: Optional[str] = None) -> None:
        """
        Initializes the MaybankPdf2Json extractor.

        Args:
            buffer (io.BufferedReader): The PDF file buffer.
            pwd (Optional[str]): The password for the PDF file.
        """
        self.buffer: io.BufferedReader = buffer
        self.pwd: Optional[str] = pwd

    def json(self) -> List[Output]:
        """
        Extracts and returns the transaction data as a list of dictionaries.

        Returns:
            List[Dict[str, Any]]: List of transaction records with keys 'date', 'desc', 'bal', and 'trans'.
        """
        return convert_to_json(self)

    def jsonV2(self) -> OutputV2:
        """
        Extracts and returns the transaction data as a dictionary.

        Returns:
            OutputV2: Dictionary containing account metadata and transaction records.
        """
        return convert_to_jsonV2(self)
