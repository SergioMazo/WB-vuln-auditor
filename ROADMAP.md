# Roadmap

Roadmap items are intentions, not commitments. They must preserve the
project's narrow, authorization-first purpose.

## 0.1.x — Reliable foundation

- Validate behavior across supported Python versions
- Add regression cases for malformed and incomplete API responses
- Improve error categories without exposing request credentials
- Document a reproducible release checklist

## 0.2.0 — Packaging and operator clarity

- Evaluate a conventional importable Python package while preserving the
  existing script entry point
- Consider explicit CLI options for existing constants
- Add structured output or exit codes for automation
- Evaluate dependency locking for release artifacts

## Later

- Add an opt-in, evidence-based CPE mapping only if device identification can
  be made reliable
- Add non-invasive integration tests against local fixtures
- Publish signed release provenance

Out of scope: password brute force, exploitation, stealth, evasion, arbitrary
port scanning, and unauthorized Internet-wide testing.
