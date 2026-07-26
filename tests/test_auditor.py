"""Behavioral tests for the scanner."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import Mock

import pytest
import requests

import Wattbox_vulnerability_comentado as auditor


def test_fetch_shodan_results_filters_invalid_matches(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    response = Mock()
    response.raise_for_status.return_value = None
    response.json.return_value = {
        "matches": [
            {"ip_str": "203.0.113.42", "port": 80},
            {"ip_str": None, "port": 80},
            {"ip_str": "203.0.113.43", "port": "80"},
            "unexpected",
        ]
    }
    get = Mock(return_value=response)
    monkeypatch.setattr(auditor.requests, "get", get)

    results = auditor.fetch_shodan_results("test-key", "wattbox port:80", 10)

    assert results == [("203.0.113.42", 80)]
    get.assert_called_once_with(
        auditor.SHODAN_SEARCH_URL,
        params={"key": "test-key", "query": "wattbox port:80"},
        timeout=auditor.API_TIMEOUT_SECONDS,
    )


def test_fetch_shodan_results_does_not_print_key_on_error(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    key = "sensitive-test-value"
    error = requests.ConnectionError(
        f"failed to reach https://api.example.invalid/?key={key}"
    )
    monkeypatch.setattr(auditor.requests, "get", Mock(side_effect=error))

    assert auditor.fetch_shodan_results(key, "query", 1) == []
    output = capsys.readouterr().out
    assert "ConnectionError" in output
    assert key not in output


def test_fetch_shodan_results_rejects_unexpected_json_root(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    response = Mock()
    response.raise_for_status.return_value = None
    response.json.return_value = ["unexpected"]
    monkeypatch.setattr(auditor.requests, "get", Mock(return_value=response))

    assert auditor.fetch_shodan_results("test-key", "query", 1) == []


@pytest.mark.parametrize(
    ("response_text", "expected"),
    [
        ("<hardware_version>WB-700</hardware_version>", "WB-700"),
        ("<hardware_version> WB-700 </hardware_version>", "WB-700"),
        ("<hardware_version></hardware_version>", None),
        ("<hardware_version>WB-700", None),
        ("unrelated", None),
    ],
)
def test_extract_hardware_version(
    response_text: str,
    expected: str | None,
) -> None:
    assert auditor._extract_hardware_version(response_text) == expected


def test_wattbox_login_returns_confirmed_result(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    response = Mock(
        status_code=200,
        text="<root><hardware_version>WB-700</hardware_version></root>",
    )
    get = Mock(return_value=response)
    monkeypatch.setattr(auditor.requests, "get", get)

    result = auditor.test_wattbox_login("203.0.113.42", 80)

    assert result == {
        "IP": "203.0.113.42",
        "Port": 80,
        "Model": "WB-700",
        "Status": "Vulnerable",
        "CVEs": "-",
    }
    get.assert_called_once_with(
        "http://203.0.113.42:80/wattbox_info.xml",
        headers=auditor.HEADERS,
        timeout=auditor.DEVICE_TIMEOUT_SECONDS,
    )


def test_wattbox_login_rejects_incomplete_response(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    response = Mock(status_code=200, text="<root />")
    monkeypatch.setattr(auditor.requests, "get", Mock(return_value=response))

    assert auditor.test_wattbox_login("203.0.113.42", 80) is None


def test_wattbox_login_handles_request_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        auditor.requests,
        "get",
        Mock(side_effect=requests.Timeout("synthetic timeout")),
    )

    assert auditor.test_wattbox_login("203.0.113.42", 80) is None


def test_cve_lookup_returns_api_records(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    cpe = "cpe:2.3:h:example:device:*:*:*:*:*:*:*:*"
    response = Mock(status_code=200)
    response.json.return_value = {"cves": [{"cve_id": "CVE-2099-0001"}]}
    get = Mock(return_value=response)
    monkeypatch.setattr(auditor.requests, "get", get)

    result = auditor.obtener_vulnerabilidades(cpe)

    assert result == [{"cve_id": "CVE-2099-0001"}]
    get.assert_called_once_with(
        auditor.SHODAN_CVEDB_URL,
        params={"cpe23": cpe},
        timeout=auditor.API_TIMEOUT_SECONDS,
    )


def test_main_requires_api_key(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(auditor, "SHODAN_API_KEY", None)

    assert auditor.main() == 2
    assert "SHODAN_API_KEY is not set" in capsys.readouterr().out


def test_main_writes_csv_for_confirmed_result(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(auditor, "SHODAN_API_KEY", "test-key")
    monkeypatch.setattr(
        auditor,
        "fetch_shodan_results",
        Mock(return_value=[("203.0.113.42", 80)]),
    )
    monkeypatch.setattr(
        auditor,
        "test_wattbox_login",
        Mock(
            return_value={
                "IP": "203.0.113.42",
                "Port": 80,
                "Model": "WB-700",
                "Status": "Vulnerable",
                "CVEs": "-",
            }
        ),
    )
    sleep = Mock()
    monkeypatch.setattr(auditor.time, "sleep", sleep)

    assert auditor.main() == 0
    output = (tmp_path / auditor.OUTPUT_FILE).read_text(encoding="utf-8")
    assert "203.0.113.42,80,WB-700,Vulnerable,-" in output
    sleep.assert_called_once_with(auditor.SCAN_DELAY_SECONDS)


def test_main_does_not_write_empty_csv(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(auditor, "SHODAN_API_KEY", "test-key")
    monkeypatch.setattr(auditor, "fetch_shodan_results", Mock(return_value=[]))

    assert auditor.main() == 0
    assert not (tmp_path / auditor.OUTPUT_FILE).exists()
