# Architecture

WB Vulnerability Auditor is intentionally a single-process command-line tool.
Its small architecture matches its narrow purpose and keeps the behavior easy
to audit.

## Data flow

```text
SHODAN_API_KEY environment variable
                |
                v
      Shodan host-search API
                |
                | matches: ip_str, port
                v
    bounded sequential device loop
                |
                | Basic Authorization header
                v
 http://target:port/wattbox_info.xml
                |
                | HTTP 200 + hardware_version
                v
       in-memory result records
                |
                +--> terminal table
                |
                +--> wattbox_vulnerables.csv
```

## Components

### Configuration constants

The script reads `SHODAN_API_KEY` from the environment. The Shodan query,
timeouts, delay, result cap, endpoint path, and output name remain code
constants to preserve the existing simple behavior.

### Shodan discovery

`fetch_shodan_results` sends one host-search request and retains valid string
IP and integer port pairs, up to the configured cap. It does not paginate.

### Device check

`test_wattbox_login` sends one HTTP GET request per match with the documented
default Basic Authentication value. A device is recorded only when the
response is HTTP 200 and contains a complete, non-empty `hardware_version`
element.

### CVE helper

`obtener_vulnerabilidades` can query Shodan CVEDB for a supplied CPE. The
normal scan does not call it because no reliable CPE is derived from the
current device response. This avoids presenting speculative CVE matches as
evidence.

### Reporting

Results remain in memory until the scan ends. Pandas renders the terminal table
and writes the CSV. No CSV is created when the result set is empty.

## Trust boundaries

- The Shodan response is external and untrusted.
- Device HTTP responses are external and untrusted.
- The API key is sensitive operator input.
- The default WattBox credential is documented product behavior, not a secret.
- The generated CSV contains sensitive assessment data and is excluded from
  version control.

## Non-goals

The architecture does not include concurrency, brute force, arbitrary target
input, exploit execution, stealth, persistence, or generalized vulnerability
scanning.
