# Contributing

Thanks for contributing to this project.

## Local Setup

1. Clone the repository.
2. Install dependencies:

```bash
make install
```

## Run Tests

Primary command:

```bash
make test
```

Alternative command:

```bash
pytest tests/
```

## Code Guidelines

- Keep changes small and focused.
- Preserve the public API: `from maybankpdf2json import MaybankPdf2Json`.
- Keep transaction schema stable: `date`, `desc`, `trans`, `bal`.
- Keep date format as `dd/mm/yy`.
- Keep trailing sign parsing behavior (`123.45-`, `123.45+`).

## Tests and Fixtures

- Integration tests require two things that are **never committed to git**:
  - `tests/test.pdf` — your personal Maybank statement (listed in `.gitignore`)
  - `TEST_PDF_PASSWORD` — the PDF password, set as an environment variable
- To run the full test suite locally, create a `.env` file or export the variables:
  ```sh
  export TEST_PDF_PASSWORD="your_pdf_password"
  export TEST_ACCOUNT_NUMBER="xxxxxx-xxxxxx"   # optional, skipped if unset
  export TEST_STATEMENT_DATE="dd/mm/yy"        # optional, skipped if unset
  ```
- If the PDF or `TEST_PDF_PASSWORD` is not present, integration tests are automatically skipped.
- `TestParserEdgeCases` uses only synthetic data and always runs without any fixture.
- If parser behavior changes, update tests together with code.

## Pull Requests

- Describe what changed and why.
- Include test results.
- Add user-facing changes to `CHANGELOG.md` under `[Unreleased]`.
- Avoid unrelated refactors in the same PR.
