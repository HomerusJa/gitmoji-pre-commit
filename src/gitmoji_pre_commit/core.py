"""Module defining the core functionality of the gitmoji-pre-commit hook."""

import re

import requests

GITMOJI_API_URL = "https://gitmoji.dev/api/gitmojis"
GITMOJI_REGEX = re.compile(
    r"^(:\w+:|[\U0001F300-\U0001F9FF\u2600-\u26FF\u2700-\u27BF][\uFE00-\uFE0F]?)",
    re.UNICODE,
)


def get_gitmoji_definitions() -> list[dict]:
    """Get the gitmoji definitions from the gitmoji API.

    The definitions look like the following:
    ```json
    [
        {
        "emoji": "⚡️",
        "entity": "&#x26a1;",
        "code": ":zap:",
        "description": "Improve performance.",
        "name": "zap",
        "semver": "patch"
        },
        ...
    ]
    ```

    Returns:
        list[dict]: The gitmoji definitions as described above.
    """
    response = requests.get(GITMOJI_API_URL)
    return response.json()["gitmojis"]


def is_valid_gitmoji_emoji(gitmoji: str, gitmoji_definitions: list[dict]) -> bool:
    """Check if a gitmoji emoji is valid.

    A gitmoji is detected if it is a unicode emoji.

    Args:
        gitmoji: The gitmoji to check.
        gitmoji_definitions: The gitmoji definitions.

    Returns:
        bool: Whether the gitmoji is valid.
    """
    return any(g["emoji"] == gitmoji for g in gitmoji_definitions)


def is_valid_gitmoji_code(gitmoji_code: str, gitmoji_definitions: list[dict]) -> bool:
    """Check if a gitmoji code is valid.

    A gitmoji is detected if it is a code following the :name: syntax.

    Args:
        gitmoji_code: The gitmoji code to check.
        gitmoji_definitions: The gitmoji definitions.

    Returns:
        bool: Whether the gitmoji code is valid.
    """
    return any(g["code"] == gitmoji_code for g in gitmoji_definitions)


def check_commit_message(
    commit_message: str,
    only_emoji: bool = False,
    only_code: bool = False,
) -> tuple[bool, str]:
    """Check if the commit message contains a gitmoji."""
    if only_emoji and only_code:
        raise ValueError("only_emoji and only_code cannot both be True")

    match = GITMOJI_REGEX.search(commit_message)
    if not match:
        return False, "Commit message must start with a gitmoji"

    emoji = match.group(0)
    gitmoji_definitions = get_gitmoji_definitions()

    contains_valid_emoji = is_valid_gitmoji_emoji(emoji, gitmoji_definitions)
    contains_valid_code = is_valid_gitmoji_code(emoji, gitmoji_definitions)

    # If only checking for emoji and we have a valid emoji, return True
    if only_emoji and contains_valid_emoji:
        return True, ""

    # If only checking for code and we have a valid code, return True
    if only_code and contains_valid_code:
        return True, ""

    # If not using exclusive checks, either a valid emoji or code is acceptable
    if (
        not only_emoji
        and not only_code
        and (contains_valid_emoji or contains_valid_code)
    ):
        return True, ""

    # Handle error messages
    if only_emoji and not contains_valid_emoji:
        return (
            False,
            "Commit message must start with a gitmoji emoji"
            + (
                " It does however contain a valid gitmoji code"
                if contains_valid_code
                else ""
            ),
        )
    if only_code and not contains_valid_code:
        return (
            False,
            "Commit message must start with a gitmoji code"
            + (
                " It does however contain a valid gitmoji emoji"
                if contains_valid_emoji
                else ""
            ),
        )

    return (
        False,
        "The emoji or code in the commit message could not be found in the gitmoji "
        "definitions.",
    )
