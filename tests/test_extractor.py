import unittest
import io
from unittest.mock import patch
from maybankpdf2json.extractor import MaybankPdf2Json


class TestExtractor(unittest.TestCase):

    def setUp(self):
        self.test_pdf_path = "a.pdf"  # Update with actual test PDF path
        self.test_password = "04Nov1997"  # Update with actual test password
        self.extractor = MaybankPdf2Json(self.test_pdf_path, self.test_password)
        print("Extractor initialized with PDF path:", self.extractor.json())


if __name__ == "__main__":
    unittest.main()
