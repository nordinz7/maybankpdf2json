# maybankpdf2json

A small Python library to extract transaction data from Maybank PDF account statements.

## Install

Requires Python 3.8 or newer.

```bash
pip install maybankpdf2json
```

## Quick Start

```python
from maybankpdf2json import MaybankPdf2Json

with open("statement.pdf", "rb") as f:
    extractor = MaybankPdf2Json(f, "your_pdf_password")

    # Raw Python data
    transactions = extractor.data()
    print(transactions[0])

    # Nicely formatted JSON string
    print(extractor.dumps())

    # Full output with account metadata
    print(extractor.dumps_v2())
```

## API

### `MaybankPdf2Json(buffer, pwd)`

- `json()` -> `List[Output]`
  - Returns transaction rows with fields: `date`, `desc`, `trans`, `bal`.
- `data()` -> `List[Output]`
  - Clearer alias for `json()`.
- `jsonV2()` -> `dict`
  - Returns:
    - `account_number`: statement account number when available
    - `statement_date`: statement date in `dd/mm/yy`
    - `transactions`: same list as `json()`
- `data_v2()` -> `dict`
  - Clearer alias for `jsonV2()`.
- `dumps(indent=2)` -> `str`
  - Returns transaction data as nicely formatted JSON text.
- `dumps_v2(indent=2)` -> `str`
  - Returns account metadata plus transactions as nicely formatted JSON text.

## Output Notes

- Dates use `dd/mm/yy`.
- Amounts support trailing sign notation from statements:
  - `123.45-` -> `-123.45`
  - `123.45+` -> `123.45`

Example pretty-printed output:

Transaction list output from `dumps()`:

```json
[
  {
    "date": "01/09/24",
    "desc": "BEGINNING BALANCE",
    "trans": 0,
    "bal": 3285.77
  },
  {
    "date": "01/09/24",
    "desc": "TRANSFER FROM A/C MBBQR1714285 * 11111755387009 124998670Q",
    "trans": -10.0,
    "bal": 3275.77
  }
]
```

Full output from `dumps_v2()`:

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

## Development

Install project dependencies:

```bash
make install
```

Run tests:

```bash
make test
```

Alternative test command:

```bash
pytest tests/
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for development workflow and [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for parser internals.

## Release

```bash
make release
```

This builds and uploads to PyPI using Twine. Run only with valid release credentials.

## License

MIT. See `LICENSE`.
