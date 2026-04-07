import unittest
import io
from datetime import datetime
from unittest.mock import patch
from maybankpdf2json.extractor import MaybankPdf2Json
from maybankpdf2json.utils import (
    get_account_number,
    get_filtered_data,
    get_mapped_data,
    get_statement_date,
    get_transactions,
)
import os
from dotenv import load_dotenv

load_dotenv()

_PDF_PATH = os.path.join(os.path.dirname(__file__), "test.pdf")
_PDF_PASSWORD = os.environ.get("TEST_PDF_PASSWORD")
_ACCOUNT_NUMBER = os.environ.get("TEST_ACCOUNT_NUMBER")
_STATEMENT_DATE = os.environ.get("TEST_STATEMENT_DATE")

_PDF_AVAILABLE = os.path.exists(_PDF_PATH) and bool(_PDF_PASSWORD)


@unittest.skipUnless(
    _PDF_AVAILABLE,
    "Provide tests/test.pdf and set TEST_PDF_PASSWORD to run integration tests",
)
class TestExtractor(unittest.TestCase):
    def setUp(self):
        with open(_PDF_PATH, "rb") as f:
            self.extractor = MaybankPdf2Json(f, _PDF_PASSWORD)
            self.payload = self.extractor.json()
            self.transactions = self.payload["transactions"]

    def test_output_structure(self):
        self.assertIsInstance(self.payload, dict)
        self.assertIn("account_number", self.payload)
        self.assertIn("statement_date", self.payload)
        self.assertIn("transactions", self.payload)
        self.assertIsInstance(self.payload["transactions"], list)

    @unittest.skipUnless(
        _ACCOUNT_NUMBER and _STATEMENT_DATE,
        "Set TEST_ACCOUNT_NUMBER and TEST_STATEMENT_DATE to run",
    )
    def test_account_metadata(self):
        self.assertEqual(self.payload["account_number"], _ACCOUNT_NUMBER)
        self.assertEqual(self.payload["statement_date"], _STATEMENT_DATE)

    def test_transaction_count(self):
        self.assertGreater(len(self.transactions), 0)

    def test_first_item_keys_and_types(self):
        self.assertGreater(len(self.transactions), 0)
        first = self.transactions[0]
        self.assertIn("desc", first)
        self.assertIn("bal", first)
        self.assertIn("trans", first)
        self.assertIn("date", first)
        self.assertIsInstance(first["desc"], str)
        self.assertIsInstance(first["bal"], float)
        self.assertIsInstance(first["trans"], (int, float))
        self.assertIsInstance(first["date"], str)

    def test_first_transaction_values(self):
        first = self.transactions[0]
        self.assertTrue(first["desc"].strip())
        self.assertIsInstance(first["bal"], float)
        self.assertIsInstance(first["trans"], (int, float))
        datetime.strptime(first["date"], "%d/%m/%y")

    def test_specific_transaction(self):
        for t in self.transactions:
            self.assertIn("desc", t)
            self.assertIn("bal", t)
            self.assertIn("trans", t)
            self.assertIn("date", t)
            self.assertTrue(t["desc"].strip())
            self.assertIsInstance(t["bal"], float)
            self.assertIsInstance(t["trans"], (int, float))
            datetime.strptime(t["date"], "%d/%m/%y")


class TestParserEdgeCases(unittest.TestCase):
    def test_get_mapped_data_handles_malformed_and_continuation_lines(self):
        raw_lines = [
            "BEGINNING BALANCE 1,000.00+",
            "",
            "MALFORMED HEADER LINE",
            "01/09/24 PAYMENT TO MERCHANT 10.00- 990.00+",
            "additional description line",
            "02/09/24 ATM WITHDRAWAL 5.00- 985.00+",
        ]

        result = get_mapped_data(raw_lines)

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]["desc"], "BEGINNING BALANCE")
        self.assertEqual(result[0]["bal"], 1000.0)
        self.assertEqual(result[0]["date"], "01/09/24")

        self.assertEqual(
            result[1]["desc"], "PAYMENT TO MERCHANT additional description line"
        )
        self.assertEqual(result[1]["trans"], -10.0)
        self.assertEqual(result[1]["bal"], 990.0)

    def test_get_filtered_data_excludes_notes_and_totals(self):
        lines = [
            "Statement Header",
            "BEGINNING BALANCE 1,000.00+",
            "Perhation / Note",
            "This note block should be removed",
            "ENTRY DATE TRANSACTION DESCRIPTION TRANSACTION AMOUNT STATEMENT BALANCE",
            "01/09/24 PAYMENT TO MERCHANT 10.00- 990.00+",
            "TOTAL CREDIT 0.00",
            "TOTAL DEBIT 10.00",
            "Footer",
        ]

        filtered = get_filtered_data(lines)

        self.assertIn("BEGINNING BALANCE 1,000.00+", filtered)
        self.assertIn("01/09/24 PAYMENT TO MERCHANT 10.00- 990.00+", filtered)
        self.assertNotIn("Perhation / Note", filtered)
        self.assertNotIn("This note block should be removed", filtered)
        self.assertNotIn("TOTAL CREDIT 0.00", filtered)
        self.assertNotIn("TOTAL DEBIT 10.00", filtered)

    def test_get_account_number_and_statement_date_helpers(self):
        lines = [
            "Random Header",
            "Account No: 162021-851156",
            "Statement Date: 30/09/24",
        ]

        self.assertEqual(get_account_number(lines), "162021-851156")
        self.assertEqual(get_statement_date(lines), "30/09/24")

    def test_get_transactions_helpers(self):
        lines = [
            "Header",
            "BEGINNING BALANCE 1,000.00+",
            "01/09/24 PAYMENT TO MERCHANT 10.00- 990.00+",
            "TOTAL DEBIT 10.00",
        ]

        transactions = get_transactions(lines)

        self.assertEqual(len(transactions), 2)
        self.assertEqual(transactions[1]["desc"], "PAYMENT TO MERCHANT")

    def test_extractor_metadata_accessor_methods(self):
        fake_pdf = b"%PDF-1.4 fake content"
        lines = ["Account No: 162021-851156", "Statement Date: 30/09/24"]

        with patch("maybankpdf2json.extractor.read", return_value=lines):
            extractor = MaybankPdf2Json(io.BytesIO(fake_pdf), None)

            self.assertEqual(extractor.get_account_number(), "162021-851156")
            self.assertEqual(extractor.get_statement_date(), "30/09/24")

    def test_extractor_transaction_accessor_methods(self):
        fake_pdf = b"%PDF-1.4 fake content"
        lines = [
            "Header",
            "BEGINNING BALANCE 1,000.00+",
            "01/09/24 PAYMENT TO MERCHANT 10.00- 990.00+",
            "TOTAL DEBIT 10.00",
        ]

        with patch("maybankpdf2json.extractor.read", return_value=lines):
            extractor = MaybankPdf2Json(io.BytesIO(fake_pdf), None)

            self.assertEqual(len(extractor.get_transactions()), 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
