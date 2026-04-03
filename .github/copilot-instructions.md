# Project Guidelines

## Code Style

- Keep changes small and focused in this library package.
- Follow existing Python style in this repo: type hints are used in public functions and key internals.
- Preserve the public API surface exported by `maybankpdf2json/__init__.py` (`MaybankPdf2Json`).
- Prefer extending parsing behavior in `maybankpdf2json/utils.py` via small helper functions instead of large rewrites.

## Architecture

- Main entry point: `MaybankPdf2Json` in `maybankpdf2json/extractor.py`.
- `MaybankPdf2Json.json()` returns `List[Output]` transactions through `convert_to_json`.
- `MaybankPdf2Json.jsonV2()` returns account metadata plus transactions through `convert_to_jsonV2`.
- PDF reading and line parsing are concentrated in `maybankpdf2json/utils.py`:
  - `read(...)` opens PDF pages with `pdfplumber`.
  - `get_filtered_data(...)` narrows raw lines to transaction content.
  - `get_mapped_data(...)` converts filtered lines into structured records.

## Build and Test

- Install dependencies: `make install` (or `pip install -r requirements.txt`).
- Run tests: `make test` (uses `python3 -m unittest discover -s tests`).
- Alternate test command documented in `README.md`: `pytest tests/`.
- Package build metadata lives in `pyproject.toml` and `setup.py`; keep both consistent when editing packaging fields.
- `make release` uploads to PyPI via Twine. Do not run release/upload commands unless explicitly requested.

## Conventions

- Preserve transaction schema fields and semantics: `date`, `desc`, `trans`, `bal`.
- Amount parsing uses trailing sign notation in statements (`123.45-`, `123.45+`) via `parse_acc_value(...)`; keep this behavior.
- Date parsing is in `dd/mm/yy` format throughout extraction paths.
- Tests in `tests/test_extractor.py` rely on fixture file `tests/test.pdf` and a known password; avoid changing fixture assumptions unless tests are updated accordingly.
- Source of truth for usage examples and user-facing behavior: `README.md`.
