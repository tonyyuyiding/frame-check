# TODO: this file is a placeholder for CLI testing.

import argparse
import sys
from pathlib import Path

from .checker import check
from .models import Severity
from .ui import format_diagnostic


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser for frame-check CLI.

    Returns:
        Configured ArgumentParser instance.
    """
    parser = argparse.ArgumentParser(
        prog="frame-check",
        description="A static checker for dataframes!",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "files",
        type=str,
        nargs="*",
        help="Python files (file.py), directories (dir/) or glob patterns (dir/**/*.py) to check. Directories will be searched recursively by default.",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args(argv)

    if not args.files:
        parser.print_help(sys.stderr)
        return 0

    file = Path(args.files[0])
    has_error = False

    for err in check(file):
        print(format_diagnostic(file, err))
        if err.category == Severity.ERROR:
            has_error = True

    return 1 if has_error else 0
