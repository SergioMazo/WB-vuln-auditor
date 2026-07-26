# Limitations

- The scanner uses one fixed Shodan query: `wattbox port:80`.
- It processes one API response and does not implement pagination.
- `MAX_RESULTS` is a local cap, not a guarantee that Shodan returns that many
  matches in one response.
- Device requests are sequential and use a fixed one-second delay.
- The device endpoint uses unencrypted HTTP because that is the behavior being
  assessed; network observers could see target metadata and the Basic
  Authentication header.
- The check covers only the documented default credentials.
- A result requires HTTP 200 and a complete `hardware_version` element.
- The XML-like response is handled with narrow tag extraction rather than a
  general XML parser.
- IPv6 URL formatting is not handled explicitly and remains untested.
- CVE enrichment is inactive because the scanner has no reliable CPE mapping.
- A request error produces a warning and an empty result for that operation;
  the final empty-result message alone is not proof that no exposure exists.
- No live target is used in tests. Network, Shodan plan, device, and firmware
  differences require authorized operational validation.
- The tool does not replace asset inventory, credential rotation, firmware
  review, network segmentation, or a complete vulnerability assessment.
