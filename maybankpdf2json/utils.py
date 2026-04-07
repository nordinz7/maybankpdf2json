import io
import re
from datetime import datetime
from typing import Any, List, Optional, TypedDict

import pdfplumber

START_ENTRY = "BEGINNING BALANCE"
END_ENTRY = "TOTAL DEBIT"
NOTE_START_ENTRY = "Perhation / Note"
NOTE_END_ENTRY = (
    "ENTRY DATE TRANSACTION DESCRIPTION TRANSACTION AMOUNT STATEMENT BALANCE"
)
EXCLUDE_ITEMS = ["TOTAL CREDIT", "TOTAL DEBIT", "ENDING BALANCE"]
DATE_FORMAT = "%d/%m/%y"
ACCOUNT_NUMBER_PATTERN = re.compile(r"\b\d{6}-\d{6}\b")
STATEMENT_DATE_PATTERN = re.compile(r"\b\d{2}/\d{2}/\d{2}\b")


class Output(TypedDict):
    date: str
    desc: str
    bal: float
    trans: float


def parse_acc_value(value: str) -> float:
    """
    Parses a string representing an account value and returns it as a float.
    Handles trailing '-' for negative and '+' for positive values.

    Args:
        value (str): The string value to parse.
    Returns:
        float: The parsed float value.
    """
    value = value.replace(",", "")
    if value.endswith("-"):
        return -float(value[:-1])
    if value.endswith("+"):
        return float(value[:-1])
    return float(value)


def is_valid_date(date_str: str) -> bool:
    """
    Checks if a string is a valid date in the format 'dd/mm/yy'.

    Args:
        date_str (str): The date string to validate.
    Returns:
        bool: True if valid, False otherwise.
    """
    try:
        datetime.strptime(date_str, DATE_FORMAT)
        return True
    except ValueError:
        return False


def get_mapped_data(arr: List[str]) -> List[Output]:
    """
    Maps raw text lines to structured Output dictionaries.

    Args:
        arr (List[str]): List of text lines from the PDF.
    Returns:
        List[Output]: List of structured transaction records.
    """
    if not arr:
        return []

    narr: List[Output] = []
    i = 0
    while i < len(arr):
        current = arr[i].strip()
        splitted = current.split()
        if not splitted:
            i += 1
            continue

        obj: Output = {"desc": "", "bal": 0, "trans": 0, "date": ""}

        # First row is opening balance metadata in Maybank statements.
        if i == 0:
            if len(splitted) >= 3:
                obj["desc"] = " ".join(splitted[0:2])
                obj["bal"] = parse_acc_value(splitted[2])
                narr.append(obj)
            i += 1
            continue

        if not is_valid_date(splitted[0]) or len(splitted) < 3:
            i += 1
            continue

        if is_valid_date(splitted[0]):
            obj["date"] = splitted[0]
            obj["trans"] = parse_acc_value(splitted[-2])
            obj["bal"] = parse_acc_value(splitted[-1])
            obj["desc"] = " ".join(splitted[1:-2])
            i += 1

            while i < len(arr):
                next_tokens = arr[i].split()
                if next_tokens and is_valid_date(next_tokens[0]):
                    break

                continuation = " ".join(next_tokens).strip()
                if continuation:
                    obj["desc"] = (obj["desc"] + " " + continuation).strip()
                i += 1

            narr.append(obj)
            continue

        i += 1

    if narr and not narr[0]["date"]:
        first_transaction_date = next(
            (row["date"] for row in narr[1:] if row["date"]), ""
        )
        if first_transaction_date:
            narr[0]["date"] = datetime.strptime(
                first_transaction_date, DATE_FORMAT
            ).strftime("01/%m/%y")

    return narr


def expand_ranges(arr: List[int]) -> List[int]:
    """
    Expands a list of index pairs into a flat list of indices.

    Args:
        arr (List[int]): List of indices (start, end, ...).
    Returns:
        List[int]: Expanded list of indices.
    """
    expanded: List[int] = []
    for ar in range(0, len(arr) - 1, 2):
        f = arr[ar]
        s = arr[ar + 1]
        for i in range(f, s + 1):
            expanded.append(i)

    if len(arr) % 2 == 1:
        expanded.append(arr[-1])

    return expanded


def get_filtered_data(arr: List[str]) -> List[str]:
    """
    Filters out non-transaction lines and note sections from the PDF text lines.

    Args:
        arr (List[str]): List of text lines from the PDF.
    Returns:
        List[str]: Filtered list of transaction lines.
    """
    indexes = [0, len(arr)]
    for i, x in enumerate(arr):
        if x.startswith(START_ENTRY):
            indexes[0] = i
        elif x.startswith(END_ENTRY):
            indexes[1] = i + 1
            break
    filtered = arr[indexes[0] : indexes[1]]
    narr: List[str] = []
    in_notes = False

    for value in filtered:
        if value.startswith(NOTE_START_ENTRY):
            in_notes = True
            continue

        if value.startswith(NOTE_END_ENTRY):
            in_notes = False
            continue

        if in_notes:
            continue

        if any(value.startswith(item) for item in EXCLUDE_ITEMS):
            continue

        narr.append(value)

    return narr


def read(buf: io.BufferedReader, pwd: Optional[str] = None) -> List[str]:
    """
    Reads text lines from a PDF file buffer using pdfplumber.

    Args:
        buf (io.BufferedReader): The PDF file buffer.
        pwd (Optional[str]): The password for the PDF file.
    Returns:
        List[str]: List of text lines from all pages.
    """
    buf.seek(0)
    with pdfplumber.open(buf, password=pwd) as pdf:
        lines: List[str] = []
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            lines.extend(page_text.splitlines())
        return lines


def convert_to_json(s: Any) -> List[Output]:
    """
    Converts a PDF statement to a list of transaction records in JSON format.

    Args:
        s (MaybankPdf2Json): An object with a 'buffer' attribute and optional 'pwd' attribute.
    Returns:
        List[Output]: List of transaction records.
    """
    all_lines = read(s.buffer, pwd=getattr(s, "pwd", None))
    d = get_filtered_data(all_lines)
    return get_mapped_data(d)


class OutputV2(TypedDict):
    account_number: Optional[str]
    statement_date: Optional[str]
    transactions: List[Output]


def get_account_number(lines: List[str]) -> Optional[str]:
    """
    Returns the first account number found in statement lines.

    Args:
        lines (List[str]): Raw statement lines.
    Returns:
        Optional[str]: Account number in NNNNNN-NNNNNN format, if found.
    """
    for line in lines:
        account_match = ACCOUNT_NUMBER_PATTERN.search(line)
        if account_match:
            return account_match.group()
    return None


def get_statement_date(lines: List[str]) -> Optional[str]:
    """
    Returns the first valid statement date found in statement lines.

    Args:
        lines (List[str]): Raw statement lines.
    Returns:
        Optional[str]: Date string in dd/mm/yy format, if found.
    """
    for line in lines:
        date_match = STATEMENT_DATE_PATTERN.search(line)
        if not date_match:
            continue

        raw_date = date_match.group()
        try:
            dt = datetime.strptime(raw_date, DATE_FORMAT)
            return dt.strftime(DATE_FORMAT)
        except ValueError:
            continue
    return None


def extract_account_and_date(lines: List[str]) -> dict:
    """
    Extracts the account number and statement date from the provided lines.
    Returns a dict with string or None values.
    """
    return {
        "account_number": get_account_number(lines),
        "statement_date": get_statement_date(lines),
    }


def get_transactions(lines: List[str]) -> List[Output]:
    """
    Returns mapped transaction rows from raw statement lines.

    Args:
        lines (List[str]): Raw statement lines.
    Returns:
        List[Output]: Parsed transactions.
    """
    filtered = get_filtered_data(lines)
    return get_mapped_data(filtered)


def convert_to_jsonV2(s: Any) -> OutputV2:
    """
    Converts a PDF statement

    Args:
        s (MaybankPdf2Json): An object with a 'buffer' attribute and optional 'pwd' attribute.
    Returns:
        {
            "account_number": str,
            "statement_date": str,
            "transactions": List[Output]
        }
    """
    all_lines = read(s.buffer, pwd=getattr(s, "pwd", None))
    transactions = get_transactions(all_lines)
    output = extract_account_and_date(all_lines)
    return {
        "account_number": output["account_number"],
        "statement_date": output["statement_date"],
        "transactions": transactions,
    }
