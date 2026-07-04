"""Basic checks that the MatchCast package is importable."""

import matchcast


def test_package_import() -> None:
    """The project package should be available through the configured src layout."""
    assert matchcast.__name__ == "matchcast"
