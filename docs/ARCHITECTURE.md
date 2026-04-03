# Architecture

This library extracts transactions from Maybank PDF statements.

## Entry Point

- `MaybankPdf2Json` in `maybankpdf2json/extractor.py` is the public interface.
- `json()` returns transaction list.
- `jsonV2()` returns account metadata plus transactions.

## Parsing Pipeline

The parsing pipeline is implemented in `maybankpdf2json/utils.py`:

1. `read(...)`
   - Reads all PDF pages using `pdfplumber` and returns plain text lines.
2. `get_filtered_data(...)`
   - Narrows lines to statement transaction region.
   - Excludes note blocks and total summary lines.
3. `get_mapped_data(...)`
   - Converts filtered lines into structured transaction records.
4. `extract_account_and_date(...)`
   - Extracts account number and statement date for `jsonV2()`.

## Data Contract

Transaction output fields:

- `date`: string in `dd/mm/yy`
- `desc`: transaction description
- `trans`: transaction amount (float)
- `bal`: balance amount (float)

Amount parsing supports statement-style trailing signs:

- `100.00-` means `-100.00`
- `100.00+` means `100.00`

## Test Coverage

- Core behaviors are validated in `tests/test_extractor.py`.
- Fixture-based tests rely on `tests/test.pdf`.
