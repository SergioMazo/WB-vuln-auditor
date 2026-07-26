# Security Policy

## Supported versions

Security fixes are provided for the `main` branch and the latest tagged
release while the project remains experimental.

## Reporting a vulnerability

Do not open a public issue for a weakness that could expose credentials,
assessment results, target data, or enable unauthorized device access.

Use GitHub private vulnerability reporting for this repository. Include:

- the affected commit or version;
- a minimal reproduction using synthetic data;
- expected impact;
- a safe mitigation;
- whether any credential or real target data may have been exposed.

Do not include live API keys, device credentials, real IP addresses, client
names, or unredacted logs. No response-time guarantee is made.

## Security boundaries

Security-sensitive areas include:

- Shodan API key handling and error messages;
- target authorization and scope control;
- HTTP authentication headers;
- generated CSV data;
- URL and response parsing;
- dependency and GitHub Actions supply-chain integrity;
- accidental live network access in tests.

The documented WattBox default credential embedded in the scanner is public
product behavior, not a repository secret. It must not be replaced with a
credential obtained from a real system.
