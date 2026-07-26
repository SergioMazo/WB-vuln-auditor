# Contributing

Thank you for helping improve WB Vulnerability Auditor.

## Scope

This project intentionally performs one narrow defensive check. Contributions
must not add brute force, exploitation, persistence, stealth, evasion, mass
targeting, or collection unrelated to confirming the documented default
credentials on explicitly authorized WattBox devices.

## Before opening a change

1. Search existing issues and keep the proposed scope small.
2. Do not include real API keys, target addresses, device output, credentials,
   or client information.
3. Explain how authorization and operator safety are preserved.
4. Add or update offline tests and documentation.
5. Avoid live network requests in the test suite.

## Development setup

```bash
git clone https://github.com/SergioMazo/WB-vuln-auditor.git
cd WB-vuln-auditor
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

Run the local checks:

```bash
make test
make lint
make shellcheck
make markdownlint
make audit
make secret-scan
```

`make shellcheck` reports that there are no targets when the repository
contains no shell files. Python code is checked by Ruff.

## Pull requests

Describe:

- the problem and intended behavior;
- why the change stays within the defensive scope;
- tests and platforms used;
- security, privacy, and compatibility considerations;
- any user-visible documentation changes.

Keep the existing script entry point compatible unless a migration has been
discussed first.
