"""Module defining the CLI for the gitmoji-pre-commit hook."""

import argparse
import sys

from . import __version__


def main(argv: list[str] | None = None) -> int:
    """Entry point for the gitmoji-pre-commit hook.

    Args:
        argv: List of arguments to parse. Defaults to sys.argv[1:].

    Returns:
        int: The exit code of the hook.
    """
    parser = argparse.ArgumentParser(
        description=(
            "A pre-commit hook ensuring commit messages follow the gitmoji "
            "convention."
        )
    )
    parser.add_argument("--version", action="version", version=__version__)
    args = parser.parse_args(argv)  # noqa: F841
    # TODO: Implement the hook logic here
    return 0


if __name__ == "__main__":
    sys.exit(main())
