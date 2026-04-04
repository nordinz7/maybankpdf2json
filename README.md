# maybankpdf2json

[![PyPI version](https://img.shields.io/pypi/v/maybankpdf2json.svg)](https://pypi.org/project/maybankpdf2json/)
[![CI](https://github.com/nordinz7/maybankpdf2json/actions/workflows/publish.yml/badge.svg)](https://github.com/nordinz7/maybankpdf2json/actions/workflows/publish.yml)

Convert Maybank PDF statements into structured data.

## TL;DR

- Use one method: `json()`
- Output includes: `account_number`, `statement_date`, `transactions`

## Install

```bash
pip install maybankpdf2json
```

## Usage

```python
from maybankpdf2json import MaybankPdf2Json

with open("statement.pdf", "rb") as f:
  data = MaybankPdf2Json(f, "your_pdf_password").json()  # No password? Omit the second argument.

print(data)
```

Example output:

```json
{
  "account_number": "162021-851156",
  "statement_date": "30/09/24",
  "transactions": [
    {
      "date": "01/09/24",
      "desc": "BEGINNING BALANCE",
      "trans": 0,
      "bal": 3285.77
    }
  ]
}
```

## Response Schema

### Root Object

| Field | Type | Format | Notes |
| --- | --- | --- | --- |
| `account_number` | `str \| None` | `NNNNNN-NNNNNN` | May be `None` if not detected |
| `statement_date` | `str \| None` | `dd/mm/yy` | May be `None` if not detected |
| `transactions` | `list[Transaction]` | Array | Ordered as parsed from statement |

### Transaction Object

| Field | Type | Format | Example |
| --- | --- | --- | --- |
| `date` | `str` | `dd/mm/yy` | `01/09/24` |
| `desc` | `str` | Free text | `BEGINNING BALANCE` |
| `trans` | `float \| int` | Signed numeric | `-10.0`, `0`, `250.5` |
| `bal` | `float` | Signed numeric | `3285.77` |

Date format is `dd/mm/yy`.

MIT License.
