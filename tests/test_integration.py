"""Integration tests for the complete gitmoji-pre-commit workflow."""

import subprocess
import tempfile
from pathlib import Path

import pytest

from gitmoji_pre_commit.cli import main


def create_temp_file(content: str) -> str:
    """Create a temporary file."""
    temp_file = tempfile.mktemp()
    Path(temp_file).write_text(content, encoding="utf-8")
    return temp_file


@pytest.mark.integration
@pytest.mark.parametrize(
    "commit_msg, exit_code",
    [
        ("⚡️ Improve performance", 0),
        (":zap: Improve performance", 0),
        ("Improve performance", 1),
        # Leave the more complex cases for unit tests
    ],
)
def test_commit_msg_hook(commit_msg: str, exit_code: int):
    """Test the gitmoji commit-msg hook."""
    commit_msg_file = create_temp_file(commit_msg)
    return_code = main(["run", commit_msg_file])
    assert return_code == exit_code


@pytest.mark.skip(reason="Doesnt work with coverage.")
@pytest.mark.integration
@pytest.mark.parametrize(
    "commit_msg, exit_code",
    [
        ("⚡️ Improve performance", 0),
        (":zap: Improve performance", 0),
        ("Improve performance", 1),
        # Leave the more complex cases for unit tests
    ],
)
def test_pre_commit_hook(commit_msg: str, exit_code: int):
    """Test the gitmoji pre-commit hook using try-repo. Doesnt work with coverage."""
    commit_msg_file = create_temp_file(commit_msg)
    process = subprocess.run(
        # fmt: off
        [
            "pre-commit",
            "try-repo",
            ".",
            "gitmoji-pre-commit",
            "--verbose",
            "--commit-msg-filename",
            commit_msg_file,
            "--hook-stage",
            "commit-msg",
        ],
        # fmt: on
        capture_output=True,
        text=True,
    )
    assert process.returncode == exit_code
