import sys
from pathlib import Path

from frame_check_core.models import Diagnostic, Severity

from .suggestion import get_suggestion

BOLD = "\033[1m"
RED = "\033[31m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RESET = "\033[0m"

GUTTER_CHAR = "|"
CARET = "^"
SPACE = " "


def format_diagnostic(source_file: Path, diagnostic: Diagnostic) -> str:
    region = diagnostic.underline_region
    support_color = bool(getattr(sys.stdout, "isatty", lambda: False)())
    lines: list[str] = []

    match diagnostic.category:
        case Severity.ERROR:
            color = RED
        case Severity.WARNING:
            color = YELLOW
        case _:
            color = None

    # header

    header_location = f"{source_file}:{region.lineno}:{region.col_offset + 1}"

    match diagnostic.category:
        case Severity.ERROR:
            header_report = f"Column {diagnostic.missing_column!r} does not exist."
        case Severity.WARNING:
            header_report = f"Column {diagnostic.missing_column!r} might not exist."
        case _:
            header_report = ""

    suggestion = get_suggestion(
        diagnostic.missing_column, diagnostic.available_columns or ()
    )
    header_suggestion = (
        f"Did you mean '{suggestion}'?" if suggestion is not None else ""
    )

    header = f"{header_location}: {header_report} {header_suggestion}"

    if support_color and color is not None:
        header = f"{BOLD}{color}{header}{RESET}"

    lines.append(header)

    # code frame

    line_width = len(str(region.lineno))
    lines.append(f"{SPACE * line_width} {GUTTER_CHAR}")

    try:
        source_code = source_file.read_text()
    except OSError:
        source_code = None

    if source_code:
        source_lines = source_code.splitlines()
        if 0 <= region.lineno - 1 < len(source_lines):
            code_line = source_lines[region.lineno - 1]
            indent = len(code_line) - len(code_line.lstrip())
            stripped_line = code_line.lstrip()
            relative_col = max(0, region.col_offset - indent)

            lines.append(f"{region.lineno:>{line_width}} {GUTTER_CHAR} {stripped_line}")

            if region.end_col_offset is None:
                underline_length = 1
            else:
                underline_length = max(1, region.end_col_offset - region.col_offset)
            caret_line = SPACE * relative_col + CARET * underline_length
            if support_color and color is not None:
                caret_line = f"{color}{caret_line}{RESET}"
            lines.append(f"{SPACE * line_width} {GUTTER_CHAR} {caret_line}")

    lines.append(f"{SPACE * line_width} {GUTTER_CHAR}")

    # available columns

    available_values = sorted((str(c) for c in diagnostic.available_columns or ()))
    available_joined = ", ".join(available_values) if available_values else "<none>"

    suggestion = f"{SPACE * line_width} = available: {available_joined}"
    if support_color:
        suggestion = f"{BLUE}{suggestion}{RESET}"

    lines.append(suggestion)

    return "\n".join(lines)
