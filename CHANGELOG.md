# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
for release version numbers.

## [Unreleased]

## [0.2.0] - 2026-04-04

### Changed

- Simplified the public extractor API to a single method: `MaybankPdf2Json.json()`.
- `json()` now returns one payload with statement metadata and transactions:
  - `account_number`
  - `statement_date`
  - `transactions`

### Removed

- Removed overlapping methods that caused API confusion:
  - `data()`
  - `jsonV2()`
  - `data_v2()`
- Removed built-in JSON rendering helpers:
  - `dumps()`
  - `dumps_v2()`

### Documentation

- Simplified README examples and API section to focus on the single output shape.
- Clarified that JSON formatting/pretty printing should be handled by user projects.

## [0.1.53] - 2026-04-04

### Added

- Automated release helpers in `Makefile` for bumping patch versions and
  publishing/tagging flow.
- CI workflows for test matrix execution and automated PyPI publish.
- Additional parser edge-case tests and pretty JSON dump test coverage.
- New maintainer documentation: `CONTRIBUTING.md`, architecture notes in
  `docs/ARCHITECTURE.md`, and changelog workflow.

### Changed

- Refined patch version bumping logic in `Makefile` and simplified release
  maintenance steps.
- Improved package exports and JSON output usability (`dumps` and `dumps_v2`
  formatting expectations covered by tests).
- Hardened parser internals while preserving output schema fields: `date`,
  `desc`, `trans`, `bal`.
- Updated dependency/package metadata and modernized README content.

### Documentation

- Expanded README with badges, quick-start/API examples, sample outputs,
  supported Python version, development commands, and release process.

### Notes

- Changelog content generated from all commits since `2026-01-01`.
- Release is documented as `0.1.53` and is pending publication to PyPI.
