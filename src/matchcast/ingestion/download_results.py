"""Download the pinned historical international-results snapshot."""

from __future__ import annotations

import argparse
import hashlib
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path
from urllib.request import urlopen

DEFAULT_COMMIT = "25e30198bc6b2e51b3cfe2efaed2d9323b37174d"
DEFAULT_URL = (
    "https://raw.githubusercontent.com/martj42/international_results/"
    f"{DEFAULT_COMMIT}/results.csv"
)
DEFAULT_SHA256 = "bcf26ebc26bd911fd8e68009c8606aa2cca09a52bde4cf739bdbddfadb014f49"
DEFAULT_DESTINATION = Path("data/raw/international_results.csv")


@dataclass(frozen=True)
class DownloadResult:
    """Metadata describing a verified download."""

    destination: Path
    sha256: str
    size_bytes: int


def calculate_sha256(path: Path) -> str:
    """Return the lowercase SHA-256 digest for a file."""
    digest = hashlib.sha256()
    with path.open("rb") as file_handle:
        for chunk in iter(lambda: file_handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download_results(
    destination: Path = DEFAULT_DESTINATION,
    *,
    source_url: str = DEFAULT_URL,
    expected_sha256: str = DEFAULT_SHA256,
    overwrite: bool = False,
) -> DownloadResult:
    """Download and verify a snapshot without leaving a partial destination."""
    destination = Path(destination)
    if destination.exists() and not overwrite:
        raise FileExistsError(
            f"{destination} already exists; pass overwrite=True to replace it"
        )

    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None

    try:
        with tempfile.NamedTemporaryFile(
            dir=destination.parent,
            prefix=f".{destination.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary_file:
            temporary_path = Path(temporary_file.name)
            with urlopen(source_url, timeout=60) as response:
                shutil.copyfileobj(response, temporary_file)

        actual_sha256 = calculate_sha256(temporary_path)
        if actual_sha256 != expected_sha256.lower():
            raise ValueError(
                "Downloaded file checksum mismatch: "
                f"expected {expected_sha256.lower()}, got {actual_sha256}"
            )

        temporary_path.replace(destination)
        temporary_path = None
        return DownloadResult(
            destination=destination,
            sha256=actual_sha256,
            size_bytes=destination.stat().st_size,
        )
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""
    parser = argparse.ArgumentParser(
        description="Download the pinned MatchCast international-results dataset."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_DESTINATION,
        help=f"destination path (default: {DEFAULT_DESTINATION})",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="replace an existing destination after verifying the new download",
    )
    return parser


def main() -> int:
    """Run the command-line downloader."""
    args = build_parser().parse_args()
    result = download_results(args.output, overwrite=args.force)
    print(
        f"Downloaded {result.size_bytes} bytes to {result.destination} "
        f"(sha256={result.sha256})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
