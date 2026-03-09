# TODO: this file is a placeholder for CLI testing.

import ast
import argparse
import sys
from pathlib import Path
from typing import Generator

from .checker import visit
from .models import VisitorContext, Diagnostic


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
    if not file.exists():
        print(f"Error: File '{file}' does not exist.", file=sys.stderr)
        return 1

    has_error = False
    context = VisitorContext()
    module: ast.Module = ast.parse(file.read_text())

    def walk(node: ast.AST) -> Generator[Diagnostic, None, None]:
        yield from visit(context, node)
        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        yield from walk(item)
            elif isinstance(value, ast.AST):
                yield from walk(value)

    for err in walk(module):
        print(err)
        has_error = True

    return 1 if has_error else 0
