# WB Vulnerability Auditor

[![Tests](https://img.shields.io/github/actions/workflow/status/SergioMazo/WB-vuln-auditor/tests.yml?branch=main&label=tests)](https://github.com/SergioMazo/WB-vuln-auditor/actions)
[![Python quality](https://img.shields.io/github/actions/workflow/status/SergioMazo/WB-vuln-auditor/python-quality.yml?branch=main&label=python%20quality)](https://github.com/SergioMazo/WB-vuln-auditor/actions)
[![Markdownlint](https://img.shields.io/github/actions/workflow/status/SergioMazo/WB-vuln-auditor/markdownlint.yml?branch=main&label=markdownlint)](https://github.com/SergioMazo/WB-vuln-auditor/actions)
[![Secret scan](https://img.shields.io/github/actions/workflow/status/SergioMazo/WB-vuln-auditor/secret-scan.yml?branch=main&label=secret%20scan)](https://github.com/SergioMazo/WB-vuln-auditor/actions)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-3776AB.svg)](https://www.python.org/)
[![Status: experimental](https://img.shields.io/badge/status-experimental-orange.svg)](ROADMAP.md)

WB Vulnerability Auditor is a focused Python utility for authorized WattBox
security assessments. It uses Shodan to locate matching HTTP services, checks
whether the documented default credentials expose `wattbox_info.xml`, records
the reported hardware version, and writes confirmed results to CSV.

It exists to make one high-value credential-hygiene check repeatable. It does
not brute-force passwords, exploit devices, scan arbitrary ports, or provide a
general-purpose vulnerability assessment.

> [!CAUTION]
> Run this tool only against systems you own or have explicit written
> authorization to assess. Internet-wide discovery and authentication attempts
> may be restricted by law, contract, or provider policy. You are responsible
> for scope, authorization, rate limits, and handling the resulting data.

## Why use it?

- Narrow scope that is easy to review and explain
- Environment-based handling of the Shodan API key
- A one-second delay between device checks
- Short device timeouts and bounded result processing
- Offline tests with no live scanning
- CSV output suitable for an authorized remediation workflow

## Architecture

```text
Authorized operator
       |
       | SHODAN_API_KEY
       v
Shodan host search
  "wattbox port:80"
       |
       | IP and port pairs
       v
HTTP GET /wattbox_info.xml
with documented default credentials
       |
       | HTTP 200 + hardware_version
       v
Terminal summary + wattbox_vulnerables.csv
```

The current scan does not perform active CVE enrichment because the device
response is not mapped to a reliable CPE. See
[Architecture](docs/architecture.md) and [Limitations](docs/limitations.md).

## Quick start

```bash
git clone https://github.com/SergioMazo/WB-vuln-auditor.git
cd WB-vuln-auditor

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

export SHODAN_API_KEY="replace_with_your_shodan_api_key"
python Wattbox_vulnerability_comentado.py
```

The application does not load `.env` files automatically. If you create one
from `.env.example`, source it explicitly and never commit it.

## Installation

Requirements:

- Python 3.10 or newer
- Your own Shodan API key with access to host search
- Network access to Shodan and the explicitly authorized target devices

Every operator must use their own Shodan account and API key. This repository
does not include, share, or pay for a key. Shodan provides an API key when an
account is created, but this project's filtered host search uses query credits.
Actual search access, quotas, and result limits therefore depend on the
operator's current Shodan account and plan.

Install only the two runtime dependencies:

```bash
python -m pip install -r requirements.txt
```

For development and local verification:

```bash
python -m pip install -r requirements-dev.txt
make check
```

## Configuration

Only the API key is externally configurable today.

| Setting | Source | Current value or purpose |
| --- | --- | --- |
| `SHODAN_API_KEY` | Environment | Required Shodan credential |
| Search query | Code constant | `wattbox port:80` |
| Result cap | Code constant | Up to 150 matches from one API response |
| Device timeout | Code constant | 3 seconds |
| Delay | Code constant | 1 second between checks |
| Output path | Code constant | `wattbox_vulnerables.csv` |

See [Configuration](docs/configuration.md) for shell examples and key-handling
guidance.

## Usage examples

Run the authorized audit:

```bash
export SHODAN_API_KEY="replace_with_your_shodan_api_key"
python Wattbox_vulnerability_comentado.py
```

Run the offline test suite without an API key:

```bash
make test
```

Check code, documentation, shell tooling, and Git history:

```bash
make check
```

## Output example

The following example uses an address reserved for documentation:

```text
[INFO] Searching Shodan for exposed WattBox devices...
[INFO] Testing 203.0.113.42:80 with default credentials...
[VULNERABLE] 203.0.113.42:80 (WB-700)
[INFO] Total tested: 1

[WARN] Devices accepting the default credentials:
           IP  Port  Model     Status CVEs
 203.0.113.42    80 WB-700 Vulnerable    -

[INFO] Results saved to wattbox_vulnerables.csv
```

The CSV contains:

```csv
IP,Port,Model,Status,CVEs
203.0.113.42,80,WB-700,Vulnerable,-
```

A row means the endpoint returned HTTP 200 with the expected hardware-version
element while using the documented defaults. It does not prove the presence of
a specific CVE. The `CVEs` field is currently `-` because CPE mapping is not
active. Read [Interpreting output](docs/output.md) before using the result in a
report.

## Security and data handling

- Never commit a real API key or a generated CSV.
- Treat discovered IP addresses, model data, and authentication results as
  sensitive assessment data.
- Confirm scope before every run; a Shodan query is not authorization.
- Rotate the Shodan API key if it appears in logs or version control.
- Report vulnerabilities through [Security policy](SECURITY.md), not a public
  issue.

The repository includes Gitleaks scanning for the complete Git history and a
test that rejects tracked RFC 1918 address literals. See
[Security model](docs/security-model.md).

## FAQ

### Do I need my own Shodan API key?

Yes. The repository never supplies or shares a Shodan credential. Create or use
your own Shodan account, obtain its API key, and confirm that the account has
host-search access and enough query credits. A free account can provide an API
key, but whether its current entitlements are sufficient for this filtered
search is controlled by Shodan and may change.

### Does this exploit WattBox devices?

No. It performs a single HTTP request to a known information endpoint using
the documented default credentials.

### Does a CSV row mean a device has a known CVE?

No. It means the default credentials were accepted and the expected hardware
field was returned. CVE enrichment is not active.

### Why can a failed Shodan request end with “no devices found”?

The scanner preserves its original simple result model. It prints a warning for
the request failure and then reports an empty result set. Review warnings before
interpreting the final line.

### Does `.env.example` load automatically?

No. Export `SHODAN_API_KEY` in the current shell or source a local `.env`
explicitly.

### Can I change the query, rate, or output path from the command line?

Not in the current version. Those values are constants in the script. CLI
configuration is a possible future improvement, not an existing feature.

## Roadmap

Near-term work focuses on better packaging, clearer machine-readable errors,
and broader test coverage without expanding the scanner's authorization or
attack surface. See [Roadmap](ROADMAP.md).

## Contributing and support

Read [Contributing](CONTRIBUTING.md), [Code of Conduct](CODE_OF_CONDUCT.md),
and [Support](SUPPORT.md) before opening an issue or pull request.

Changes must preserve the project's narrow defensive scope. New discovery,
credential-attack, exploitation, or evasion features are out of scope.

## License

WB Vulnerability Auditor is available under the [MIT License](LICENSE).

## Acknowledgements

- [Shodan](https://www.shodan.io/) provides the host-search and CVEDB services
  referenced by the project.
- WattBox is referenced only to describe the devices the tool checks. This
  project is independent and is not endorsed by Shodan or WattBox.
- MiniOps provided the quality benchmark for repository structure,
  documentation, tests, and CI discipline; no MiniOps files were copied
  verbatim.
