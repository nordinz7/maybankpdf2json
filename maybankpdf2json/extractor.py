import io
from typing import Optional

from .utils import OutputV2, convert_to_jsonV2


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

    def json(self) -> OutputV2:
        """
        Extracts and returns account metadata and transaction rows.

        Returns:
            OutputV2: Dictionary containing account metadata and transactions.
        """
        return convert_to_jsonV2(self)
