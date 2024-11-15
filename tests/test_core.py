"""Tests for the core module."""

from typing import Any

import pytest
import responses

from gitmoji_pre_commit.core import (
    check_commit_message,
    get_gitmoji_definitions,
    is_valid_gitmoji_code,
    is_valid_gitmoji_emoji,
)


@pytest.fixture
def gitmoji_definitions() -> list[dict[str, str]]:
    """Return a list of gitmoji definitions."""
    return [
        {
            "emoji": "⚡️",
            "code": ":zap:",
            "description": "Improve performance.",
            "name": "zap",
        },
        {
            "emoji": "🐛",
            "code": ":bug:",
            "description": "Fix a bug.",
            "name": "bug",
        },
    ]


@pytest.fixture
def mock_gitmoji_api(gitmoji_definitions: list[dict[str, str]]) -> Any:
    """Mock the gitmoji API."""
    with responses.RequestsMock(
        # Needed because in some cases, the function will fail before the request is
        # sent.
        assert_all_requests_are_fired=False,
    ) as rsps:
        rsps.add(
            responses.GET,
            "https://gitmoji.dev/api/gitmojis",
            json={"gitmojis": gitmoji_definitions},
            status=200,
        )
        yield rsps


@pytest.mark.parametrize(
    "emoji,expected",
    [
        ("⚡️", True),
        ("🐛", True),
        ("💩", False),
        ("", False),
    ],
)
def test_is_valid_gitmoji_emoji(
    emoji: str,
    expected: bool,
    gitmoji_definitions: list[dict[str, str]],
) -> None:
    """Test if a gitmoji emoji is valid."""
    assert is_valid_gitmoji_emoji(emoji, gitmoji_definitions) is expected


@pytest.mark.parametrize(
    "code,expected",
    [
        (":zap:", True),
        (":bug:", True),
        (":invalid:", False),
        ("", False),
    ],
)
def test_is_valid_gitmoji_code(
    code: str,
    expected: bool,
    gitmoji_definitions: list[dict[str, str]],
) -> None:
    """Test if a gitmoji code is valid."""
    assert is_valid_gitmoji_code(code, gitmoji_definitions) is expected


def test_get_gitmoji_definitions(
    mock_gitmoji_api: Any,  # noqa: ARG001
    gitmoji_definitions: list[dict[str, str]],
) -> None:
    """Test if the gitmoji definitions are fetched correctly."""
    assert get_gitmoji_definitions() == gitmoji_definitions


@pytest.mark.parametrize(
    "commit_message,expected",
    [
        ("⚡️ Improve performance", (True, "")),
        (":zap: Improve performance", (True, "")),
        (
            "Improve performance",
            (False, "Commit message must start with a gitmoji"),
        ),
        (
            "💩 Invalid emoji",
            (
                False,
                "The emoji or code in the commit message could not be found in the "
                "gitmoji definitions.",
            ),
        ),
    ],
)
def test_check_commit_message_basic_validation(
    commit_message: str,
    expected: tuple[bool, str],
    mock_gitmoji_api: Any,  # noqa: ARG001
) -> None:
    """Test if the commit message is validated correctly."""
    assert check_commit_message(commit_message) == expected


@pytest.mark.parametrize(
    "commit_message,only_emoji,only_code,expected_valid",
    [
        ("⚡️ Test message", True, False, True),
        (":zap: Test message", True, False, False),
        ("⚡️ Test message", False, True, False),
        (":zap: Test message", False, True, True),
    ],
)
def test_check_commit_message_emoji_code_flags(
    commit_message: str,
    only_emoji: bool,
    only_code: bool,
    expected_valid: bool,
    mock_gitmoji_api: Any,  # noqa: ARG001
) -> None:
    """Test if commit message validation works with emoji and code flags."""
    is_valid, _ = check_commit_message(
        commit_message, only_emoji=only_emoji, only_code=only_code
    )
    assert is_valid is expected_valid


def test_check_commit_message_mutually_exclusive_flags() -> None:
    """Test if the only_emoji and only_code flags are mutually exclusive."""
    with pytest.raises(
        ValueError, match="only_emoji and only_code cannot both be True"
    ):
        check_commit_message("test", only_emoji=True, only_code=True)
