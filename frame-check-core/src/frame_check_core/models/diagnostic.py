import ast
from dataclasses import dataclass
from enum import StrEnum
from collections.abc import Iterable

from .base import ColumnName
from .frame import FrameInstance


@dataclass(frozen=True, kw_only=True, slots=True)
class CodeRegion:
    lineno: int
    col_offset: int
    end_lineno: int | None
    end_col_offset: int | None

    @staticmethod
    def from_expr(expr: ast.expr) -> "CodeRegion":
        return CodeRegion(
            lineno=expr.lineno,
            col_offset=expr.col_offset,
            end_lineno=expr.end_lineno,
            end_col_offset=expr.end_col_offset,
        )


class Severity(StrEnum):
    WARNING = "warning"
    """The column might be present, but there is no proof."""
    ERROR = "error"
    """The column is definitely not present."""


@dataclass(frozen=True, kw_only=True, slots=True)
class Diagnostic:
    category: Severity
    missing_column: ColumnName
    underline_region: CodeRegion
    available_columns: Iterable[ColumnName] | None

    @staticmethod
    def mark_expr(
        expr: ast.expr,
        frame: FrameInstance,
        missing_column: ColumnName,
    ) -> "Diagnostic":
        return Diagnostic(
            category=Severity.WARNING if frame.maybe_more else Severity.ERROR,
            missing_column=missing_column,
            underline_region=CodeRegion.from_expr(expr),
            available_columns=frame.columns,
        )
