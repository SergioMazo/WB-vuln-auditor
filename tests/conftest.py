"""Shared test safeguards."""

from __future__ import annotations

import pytest
import requests


@pytest.fixture(autouse=True)
def block_live_network(monkeypatch: pytest.MonkeyPatch) -> None:
    """Fail every test that attempts an unmocked network request."""

    def fail_request(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("Tests must not perform live network requests")

    monkeypatch.setattr(requests.sessions.Session, "request", fail_request)
