"""Checks for sensitive artifacts and private infrastructure data."""

from __future__ import annotations

import ipaddress
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IPV4_LITERAL = re.compile(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])")


def repository_files() -> list[Path]:
    result = subprocess.run(
        [
            "git",
            "ls-files",
            "--cached",
            "--others",
            "--exclude-standard",
            "-z",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    return [
        ROOT / item.decode("utf-8")
        for item in result.stdout.split(b"\0")
        if item
    ]


def rfc1918_networks() -> tuple[ipaddress.IPv4Network, ...]:
    definitions = (
        ((10, 0, 0, 0), 8),
        ((172, 16, 0, 0), 12),
        ((192, 168, 0, 0), 16),
    )
    return tuple(
        ipaddress.ip_network(
            f"{'.'.join(str(octet) for octet in address)}/{prefix}"
        )
        for address, prefix in definitions
    )


def test_no_rfc1918_literals_are_tracked() -> None:
    findings: list[str] = []
    private_networks = rfc1918_networks()

    for path in repository_files():
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, IsADirectoryError):
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            for value in IPV4_LITERAL.findall(line):
                try:
                    address = ipaddress.ip_address(value)
                except ValueError:
                    continue
                if any(address in network for network in private_networks):
                    findings.append(
                        f"{path.relative_to(ROOT)}:{line_number}: {value}"
                    )

    assert not findings, "RFC 1918 address literals found:\n" + "\n".join(findings)


def test_sensitive_local_artifacts_are_not_tracked() -> None:
    relative_paths = {path.relative_to(ROOT).as_posix() for path in repository_files()}
    forbidden = {
        ".env",
        "wattbox_vulnerables.csv",
    }
    assert relative_paths.isdisjoint(forbidden)
