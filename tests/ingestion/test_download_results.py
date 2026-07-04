"""Tests for the historical-results downloader."""

from __future__ import annotations

import hashlib
from io import BytesIO
from pathlib import Path

import pytest

from matchcast.ingestion import download_results as downloader


def test_download_results_writes_verified_content(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Verified content should be moved to the requested destination."""
    content = b"date,home_team\n2026-07-04,Canada\n"
    checksum = hashlib.sha256(content).hexdigest()
    destination = tmp_path / "raw" / "results.csv"
    monkeypatch.setattr(downloader, "urlopen", lambda *_args, **_kwargs: BytesIO(content))

    result = downloader.download_results(
        destination,
        source_url="https://example.test/results.csv",
        expected_sha256=checksum,
    )

    assert destination.read_bytes() == content
    assert result.destination == destination
    assert result.sha256 == checksum
    assert result.size_bytes == len(content)


def test_download_results_refuses_to_overwrite(tmp_path: Path) -> None:
    """An existing raw snapshot should be protected by default."""
    destination = tmp_path / "results.csv"
    destination.write_text("existing", encoding="utf-8")

    with pytest.raises(FileExistsError, match="already exists"):
        downloader.download_results(destination)

    assert destination.read_text(encoding="utf-8") == "existing"


def test_download_results_removes_bad_download(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """A checksum failure should preserve no destination or temporary file."""
    destination = tmp_path / "results.csv"
    monkeypatch.setattr(
        downloader,
        "urlopen",
        lambda *_args, **_kwargs: BytesIO(b"unexpected content"),
    )

    with pytest.raises(ValueError, match="checksum mismatch"):
        downloader.download_results(
            destination,
            source_url="https://example.test/results.csv",
            expected_sha256="0" * 64,
        )

    assert not destination.exists()
    assert list(tmp_path.iterdir()) == []
