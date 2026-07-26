# Release Checklist

## Prepare

1. Confirm `VERSION` and `CHANGELOG.md`.
2. Confirm README claims match the current code.
3. Review dependency and GitHub Actions updates.
4. Confirm the working tree contains no generated CSV or local environment
   file.

## Validate

```bash
make lint
make shellcheck
make test
make markdownlint
make audit
make secret-scan
git fsck --full
```

Also validate internal and external README links, inspect the complete diff,
and confirm all required GitHub Actions pass on the release commit.

## Release

1. Tag the exact verified commit using `v` plus the value in `VERSION`.
2. Push the tag only after branch protection and Actions are green.
3. Create release notes from `CHANGELOG.md`.
4. State the authorization requirement and experimental status.
5. Confirm the release badge and documentation links resolve.

Never create a release from an unverified or locally modified working tree.
