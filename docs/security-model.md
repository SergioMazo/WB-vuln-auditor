# Security Model

## Objective

The tool provides a repeatable check for WattBox devices that still expose a
known information endpoint through the documented default credentials. Its
value comes from narrow scope and transparent evidence, not broad offensive
capability.

## Assumptions

- The operator has explicit authorization for every target tested.
- The Shodan account and API key belong to the operator.
- The runtime host and network are trusted for the assessment.
- Shodan and device responses may be malformed or adversarial.
- Generated findings are sensitive even when the queried devices are publicly
  reachable.

## Controls

- The API key is read from the environment and never committed in an example.
- Shodan errors are reported by exception type without printing a credentialed
  request URL.
- External requests have bounded timeouts.
- Device checks are sequential with a fixed delay.
- Only one endpoint and one documented credential pair are used.
- Tests prohibit live network access.
- Generated CSV output and local environment files are ignored by Git.
- CI scans the complete Git history with Gitleaks.
- Repository hygiene tests reject tracked RFC 1918 address literals and
  sensitive local artifact names.

## Residual risks

- Basic Authentication over HTTP is observable on the network.
- Shodan discovery may return out-of-scope, stale, or incorrectly identified
  services.
- The final empty-result message can follow a request warning.
- Hardware-version text is external data and appears in terminal and CSV
  output.
- Dependency or CI action compromise remains a supply-chain risk.
- The public default credential can be misused independently of this tool.

## Operator responsibilities

Before a run, record authorization, scope, time window, rate constraints, data
handling rules, and an incident contact. After a confirmed result, follow the
approved validation and disclosure process and rotate affected credentials.

Shodan discovery is not evidence of permission to authenticate to a device.
