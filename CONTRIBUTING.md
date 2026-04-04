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

- Tests use `tests/test.pdf` and a known password in `tests/test_extractor.py`.
- If parser behavior changes, update tests together with code.

## Pull Requests

- Describe what changed and why.
- Include test results.
- Add user-facing changes to `CHANGELOG.md` under `[Unreleased]`.
- Avoid unrelated refactors in the same PR.
