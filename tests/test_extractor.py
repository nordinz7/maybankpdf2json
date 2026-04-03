import unittest
from maybankpdf2json.extractor import MaybankPdf2Json
from maybankpdf2json.utils import get_filtered_data, get_mapped_data
import os


class TestExtractor(unittest.TestCase):
    def setUp(self):
        self.test_pdf_path = os.path.join(os.path.dirname(__file__), "test.pdf")
        self.test_password = "04Nov1997"  # Update with actual test password
        with open(self.test_pdf_path, "rb") as f:
            self.extractor = MaybankPdf2Json(f, self.test_password)
            self.data = self.extractor.json()
            self.dataV2 = self.extractor.jsonV2()

    def test_output_is_list(self):
        self.assertIsInstance(self.data, list)

    def test_transaction_count(self):
        self.assertEqual(len(self.data), 47)

    def test_first_item_keys_and_types(self):
        first = self.data[0]
        self.assertIn("desc", first)
        self.assertIn("bal", first)
        self.assertIn("trans", first)
        self.assertIn("date", first)
        self.assertIsInstance(first["desc"], str)
        self.assertIsInstance(first["bal"], float)
        self.assertIsInstance(first["trans"], (int, float))
        self.assertIsInstance(first["date"], str)

    def test_first_transaction_values(self):
        first = self.data[0]
        self.assertEqual(first["desc"], "BEGINNING BALANCE")
        self.assertEqual(first["bal"], 3285.77)
        self.assertEqual(first["trans"], 0)
        self.assertEqual(first["date"], "01/09/24")

    def test_specific_transaction(self):
        t = self.data[10]
        self.assertEqual(
            t["desc"],
            "FPX PAYMENT FR A/ 2392442593 * PACIFIC & ORIENT INS 2409151125380674",
        )
        self.assertEqual(t["bal"], 2395.67)
        self.assertEqual(t["trans"], -222.1)
        self.assertEqual(t["date"], "15/09/24")

    def test_jsonV2_structure(self):
        self.assertIsInstance(self.dataV2, dict)
        self.assertIn("account_number", self.dataV2)
        self.assertIn("statement_date", self.dataV2)
        self.assertIn("transactions", self.dataV2)
        self.assertIsInstance(self.dataV2["transactions"], list)
        self.assertEqual(len(self.dataV2["transactions"]), 47)

    def test_jsonV2_account_number(self):
        self.assertEqual(self.dataV2["account_number"], "162021-851156")

    def test_jsonV2_statement_date(self):
        self.assertEqual(self.dataV2["statement_date"], "30/09/24")

    def test_jsonV2_first_transaction(self):
        first = self.dataV2["transactions"][0]
        self.assertEqual(first["desc"], "BEGINNING BALANCE")
        self.assertEqual(first["bal"], 3285.77)


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


if __name__ == "__main__":
    unittest.main()
