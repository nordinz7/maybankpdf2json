import io
import json
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
        original_position = buffer.tell()
        buffer.seek(0)
        self.buffer = io.BytesIO(buffer.read())
        buffer.seek(original_position)
        self.pwd: Optional[str] = pwd

    def json(self) -> List[Output]:
        """
        Extracts and returns the transaction data as a list of dictionaries.

        Returns:
            List[Dict[str, Any]]: List of transaction records with keys 'date', 'desc', 'bal', and 'trans'.
        """
        return convert_to_json(self)

    def data(self) -> List[Output]:
        """Return transaction rows using a clearer method name."""
        return self.json()

    def jsonV2(self) -> OutputV2:
        """
        Extracts and returns the transaction data as a dictionary.

        Returns:
            OutputV2: Dictionary containing account metadata and transaction records.
        """
        return convert_to_jsonV2(self)

    def data_v2(self) -> OutputV2:
        """Return account metadata plus transactions using a clearer method name."""
        return self.jsonV2()

    def dumps(self, indent: int = 2) -> str:
        """Serialize transaction rows as formatted JSON text."""
        return json.dumps(self.json(), indent=indent, ensure_ascii=False)

    def dumps_v2(self, indent: int = 2) -> str:
        """Serialize account metadata plus transactions as formatted JSON text."""
        return json.dumps(self.jsonV2(), indent=indent, ensure_ascii=False)
