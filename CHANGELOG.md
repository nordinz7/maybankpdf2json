# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
for release version numbers.

## [Unreleased]

## [v1.53] - 2026-04-04

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
- Release is documented as `v1.53` and is pending publication to PyPI.
