# Changelog

All notable changes to EvalOrigin are documented here. The format follows Keep
a Changelog, and the project uses semantic versioning.

## [Unreleased]

### Changed

- Gate wording is under review for the next patch.

## [1.0.2] - 2026-07-07

### Fixed

- The gate command reports a pack with zero cases as a usage error instead of
  a pass.

## [1.0.1] - 2025-11-11

### Fixed

- Gate exit codes distinguish "no gate declared" from "gate failed".

## [1.0.0] - 2024-10-01

### Added

- Stable CLI contract for compile, cases, rubric, fixtures, gate, report, and
  inspect, exit codes 0/1/2.
- Tests pin the compiled pack shape against the bundled fixtures.

## [0.9.0] - 2023-08-15

### Added

- Pack output: cases, rubrics, fixtures, and report in one directory.

## [0.8.0] - 2022-12-13

### Added

- Fixture compilation from incident records.

