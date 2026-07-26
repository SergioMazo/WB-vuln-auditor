# Configuration

## Shodan API key

The only runtime setting read from the environment is `SHODAN_API_KEY`.
Each operator must supply a key from their own Shodan account. The project does
not bundle, share, or sponsor API access.

Shodan provides an API key when an account is created. However, the scanner's
`wattbox port:80` query contains a filter and therefore uses Shodan query
credits. Host-search availability, quotas, and result limits depend on the
account's current plan and credits; a free account is not guaranteed to be
sufficient. Confirm the account's API entitlements before running the tool.

Export it for the current shell:

```bash
export SHODAN_API_KEY="replace_with_your_shodan_api_key"
python Wattbox_vulnerability_comentado.py
```

Or create a local file from the template:

```bash
cp .env.example .env
```

Edit `.env`, then load it explicitly:

```bash
set -a
. ./.env
set +a
python Wattbox_vulnerability_comentado.py
```

The script does not automatically read `.env`. The local file is ignored by
Git and must never be committed.

## Fixed values

The current version intentionally has no command-line configuration. These
values are constants in `Wattbox_vulnerability_comentado.py`:

| Constant | Value | Meaning |
| --- | --- | --- |
| `SHODAN_SEARCH_QUERY` | `wattbox port:80` | Shodan discovery filter |
| `MAX_RESULTS` | `150` | Maximum matches used from one response |
| `API_TIMEOUT_SECONDS` | `10` | Shodan and CVEDB request timeout |
| `DEVICE_TIMEOUT_SECONDS` | `3` | Per-device request timeout |
| `SCAN_DELAY_SECONDS` | `1` | Delay after each device check |
| `OUTPUT_FILE` | `wattbox_vulnerables.csv` | Result file |

Changing these values means editing the source and should be reviewed and
tested as a code change.

## Key handling

- Use a dedicated, least-privilege Shodan account where practical.
- Do not place the key in command history, screenshots, logs, issues, or CSV
  files.
- The scanner passes the key as a request parameter because the API requires
  it, but error output never prints the request URL.
- Rotate the key immediately if it enters Git history.
