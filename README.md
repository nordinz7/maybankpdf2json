# maybankpdf2json

A small Python library to extract transaction data from Maybank PDF account statements.

## Install

```bash
pip install maybankpdf2json
```

## Quick Start

```python
from maybankpdf2json import MaybankPdf2Json

with open("statement.pdf", "rb") as f:
    extractor = MaybankPdf2Json(f, "your_pdf_password")

    transactions = extractor.json()
    print(transactions[0])

    full_output = extractor.jsonV2()
    print(full_output["account_number"], full_output["statement_date"])
```

## API

### `MaybankPdf2Json(buffer, pwd)`

- `json()` -> `List[Output]`
  - Returns transaction rows with fields: `date`, `desc`, `trans`, `bal`.
- `jsonV2()` -> `dict`
  - Returns:
    - `account_number`: statement account number when available
    - `statement_date`: statement date in `dd/mm/yy`
    - `transactions`: same list as `json()`

## Output Notes

- Dates use `dd/mm/yy`.
- Amounts support trailing sign notation from statements:
  - `123.45-` -> `-123.45`
  - `123.45+` -> `123.45`

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
