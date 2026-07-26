## Summary

Explain the problem and the narrow change.

## Scope and safety

- [ ] The change preserves the authorization-first defensive purpose.
- [ ] It does not add brute force, exploitation, stealth, evasion, or arbitrary
  mass targeting.
- [ ] It contains no credentials, real targets, client data, or generated CSV.

## Validation

- [ ] `make test`
- [ ] `make lint`
- [ ] `make shellcheck`
- [ ] `make markdownlint`
- [ ] `make secret-scan`
- [ ] Documentation updated where behavior is user-visible

## Compatibility

Describe Python versions tested and any effect on the existing script entry
point.
