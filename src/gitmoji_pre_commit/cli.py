"""Module defining the CLI for the gitmoji-pre-commit hook."""

import argparse
import sys
from pathlib import Path

from . import __version__
from .core import check_commit_message


def run_hook(args: argparse.Namespace) -> int:
    """Handle the 'run' command.

    Args:
        args: Parsed command line arguments

    Returns:
        int: Exit code (0 for success, 1 for failure)
    """
    commit_msg = Path(args.commit_msg_file).read_text(encoding="utf-8")
    success, message = check_commit_message(
        commit_msg, only_emoji=args.only_emoji, only_code=args.only_code
    )
    if message:
        print(message)
    return 0 if success else 1


def main(argv: list[str] | None = None) -> int:
    """Entry point for the gitmoji-pre-commit hook.

    Args:
        argv: List of arguments to parse. Defaults to sys.argv[1:].

    Returns:
        int: The exit code of the hook (0 if valid, 1 if invalid).
    """
    parser = argparse.ArgumentParser(
        description=(
            "A pre-commit hook ensuring commit messages follow the gitmoji "
            "convention."
        )
    )
    parser.add_argument("--version", action="version", version=__version__)

    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser(
        "run", help="Run the gitmoji commit message check"
    )
    run_parser.add_argument("commit_msg_file", help="Path to the commit message file")
    run_parser.add_argument(
        "--only-emoji",
        action="store_true",
        help="Only allow a unicode emoji, not a code.",
    )
    run_parser.add_argument(
        "--only-code",
        action="store_true",
        help="Only allow a code, not a unicode emoji.",
    )
    run_parser.set_defaults(func=run_hook)

    args = parser.parse_args(argv)

    # Call the appropriate subcommand function
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
