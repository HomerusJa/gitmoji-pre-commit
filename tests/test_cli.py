"""Tests for the CLI module."""

import pytest

from gitmoji_pre_commit import __version__
from gitmoji_pre_commit.cli import main


def test_version_flag(capsys: pytest.CaptureFixture[str]) -> None:
    """Test that --version flag prints the correct version."""
    with pytest.raises(SystemExit) as excinfo:
        main(["--version"])

    assert excinfo.value.code == 0
    captured = capsys.readouterr()
    assert captured.out.strip() == __version__
