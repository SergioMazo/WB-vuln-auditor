PYTHON ?= python3

.PHONY: help install install-dev test lint shellcheck markdownlint audit secret-scan check

help:
	@printf '%s\n' \
	  'make install       Install runtime dependencies' \
	  'make install-dev   Install development dependencies' \
	  'make test          Run the offline test suite' \
	  'make lint          Run Ruff against Python files' \
	  'make shellcheck    Check any shell files present in the repository' \
	  'make markdownlint  Validate Markdown with markdownlint-cli2' \
	  'make audit         Audit installed runtime dependencies' \
	  'make secret-scan   Scan the complete Git history with Gitleaks' \
	  'make check         Run tests and all locally available checks'

install:
	@$(PYTHON) -m pip install -r requirements.txt

install-dev:
	@$(PYTHON) -m pip install -r requirements-dev.txt

test:
	@$(PYTHON) -m pytest

lint:
	@$(PYTHON) -m ruff check .

shellcheck:
	@command -v shellcheck >/dev/null 2>&1 || { echo 'shellcheck is required'; exit 127; }
	@files="$$(find . -type f -name '*.sh' -not -path './.git/*' -print)"; \
	if [ -n "$$files" ]; then shellcheck $$files; \
	else echo 'No shell files found; ShellCheck has no targets.'; fi

markdownlint:
	@command -v markdownlint-cli2 >/dev/null 2>&1 || { echo 'markdownlint-cli2 is required'; exit 127; }
	@markdownlint-cli2 '**/*.md' '#.git'

audit:
	@$(PYTHON) -m pip_audit --requirement requirements.txt

secret-scan:
	@command -v gitleaks >/dev/null 2>&1 || { echo 'gitleaks is required'; exit 127; }
	@gitleaks git --redact --verbose
	@gitleaks dir . --redact --verbose

check: lint shellcheck test audit secret-scan
	@if command -v markdownlint-cli2 >/dev/null 2>&1; then \
	  markdownlint-cli2 '**/*.md' '#.git'; \
	else \
	  echo 'markdownlint-cli2 not installed; Markdown lint deferred to CI'; \
	fi
