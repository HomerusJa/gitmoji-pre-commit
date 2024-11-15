"""Tests for the CLI module."""

import pytest

from gitmoji_pre_commit import __version__
from gitmoji_pre_commit.cli import main


def test_main_returns_zero() -> None:
    """Test that main returns 0 when no arguments are provided."""
    assert main() == 0


def test_version_flag(capsys: pytest.CaptureFixture[str]) -> None:
    """Test that --version flag prints the correct version."""
    with pytest.raises(SystemExit) as excinfo:
        main(["--version"])

    assert excinfo.value.code == 0
    captured = capsys.readouterr()
    assert captured.out.strip() == __version__


def test_invalid_argument(capsys: pytest.CaptureFixture[str]) -> None:
    """Test that invalid arguments raise an error."""
    with pytest.raises(SystemExit) as excinfo:
        main(["--invalid-arg"])

    assert excinfo.value.code == 2
    captured = capsys.readouterr()
    assert "error: unrecognized arguments" in captured.err
