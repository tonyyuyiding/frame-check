import ast
from dataclasses import dataclass
from enum import StrEnum

from .base import ColumnName


@dataclass(frozen=True, kw_only=True, slots=True)
class CodeRegion:
    lineno: int
    col_offset: int
    end_lineno: int | None
    end_col_offset: int | None

    @staticmethod
    def from_expr(expr: ast.Expr) -> "CodeRegion":
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
    similar_columns: tuple[ColumnName, ...] | None

    @staticmethod
    def mark_expr(
        expr: ast.Expr,
        category: Severity,
        missing_column: ColumnName,
        similar_columns: tuple[ColumnName, ...] | None = None,
    ) -> "Diagnostic":
        return Diagnostic(
            category=category,
            missing_column=missing_column,
            underline_region=CodeRegion.from_expr(expr),
            similar_columns=similar_columns,
        )
