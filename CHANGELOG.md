# Changelog

All notable changes to WB Vulnerability Auditor are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and the project intends to use [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.1.0] - 2026-07-26

### Added

- Professional project documentation and governance files
- Offline tests for Shodan parsing, device checks, CSV output, and repository
  hygiene
- Ruff, ShellCheck, Markdownlint, test, and Gitleaks automation
- Dependabot configuration and issue and pull request templates
- MIT license and initial roadmap

### Changed

- Added explicit request timeouts and safer error reporting
- Prevented Shodan API keys from being embedded directly in constructed URLs
- Replaced broad exception handling with targeted failure paths
- Clarified the exact meaning and limitations of reported results
- Added dependency compatibility ranges

### Security

- Added complete-history secret scanning
- Ignored local credentials, generated CSV output, and common key material
