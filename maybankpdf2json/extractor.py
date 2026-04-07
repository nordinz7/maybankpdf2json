import io
from typing import List, Optional

from .utils import (
    OutputV2,
    convert_to_jsonV2,
    get_account_number,
    get_statement_date,
    read,
)


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
        self._lines_cache: Optional[List[str]] = None

    def _get_all_lines(self) -> List[str]:
        """
        Lazily reads statement lines and caches them for repeated metadata access.
        """
        if self._lines_cache is None:
            self._lines_cache = read(self.buffer, pwd=self.pwd)
        return self._lines_cache

    def get_account_number(self) -> Optional[str]:
        """
        Returns account number from the statement without parsing transactions.
        """
        return get_account_number(self._get_all_lines())

    def get_statement_date(self) -> Optional[str]:
        """
        Returns statement date from the statement without parsing transactions.
        """
        return get_statement_date(self._get_all_lines())

    def json(self) -> OutputV2:
        """
        Extracts and returns account metadata and transaction rows.

        Returns:
            OutputV2: Dictionary containing account metadata and transactions.
        """
        return convert_to_jsonV2(self)
