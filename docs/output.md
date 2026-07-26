# Interpreting output

## Terminal messages

| Prefix | Meaning |
| --- | --- |
| `[INFO]` | Normal progress or summary |
| `[VULNERABLE]` | Default credentials returned the expected device metadata |
| `[WARN]` | A request, response, or security-relevant condition needs review |
| `[ERROR]` | Required configuration is missing |
| `[OK]` | No confirmed result records were produced |

An `[OK]` final line does not override earlier warnings. A Shodan failure
currently becomes an empty result set, so operators must review the complete
output before concluding that no affected devices exist.

## CSV schema

| Column | Meaning |
| --- | --- |
| `IP` | Address returned by Shodan |
| `Port` | Port returned by Shodan |
| `Model` | Text inside the `hardware_version` response element |
| `Status` | `Vulnerable` when the narrow default-credential check succeeds |
| `CVEs` | `-` because CPE-based enrichment is not active |

See [Synthetic output](../examples/example-output.csv) for the exact format.
The example uses an address reserved for documentation.

## What “Vulnerable” means

The label means all of the following occurred:

1. Shodan returned an IP and port for the fixed WattBox query.
2. The scanner sent one request to `/wattbox_info.xml` using the documented
   default Basic Authentication value.
3. The response was HTTP 200.
4. The response contained a complete, non-empty `hardware_version` element.

It does not establish:

- ownership or authorization;
- the presence or exploitability of a specific CVE;
- access to other endpoints;
- device firmware version;
- whether the finding is reachable from every network;
- whether credentials have since been changed.

## Handling findings

Treat the CSV as sensitive assessment evidence. Store it outside the
repository, restrict access, verify ownership and scope, validate the finding
through the approved process, and remove or archive it according to the
engagement's retention rules.
