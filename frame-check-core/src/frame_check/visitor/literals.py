import ast
from typing import Generator, overload

from frame_check.models import (
    ColumnName,
    is_column_name,
    _Unknown,
    Unknown,
    VisitorContext,
)


def maybe_str(ctx: VisitorContext, expr: ast.expr) -> str | _Unknown:
    match expr:
        case ast.Constant(value) if isinstance(value, str):
            return value
        case _:
            return Unknown


def maybe_column_name(ctx: VisitorContext, expr: ast.expr) -> ColumnName | _Unknown:
    match expr:
        case ast.Constant(value) if is_column_name(value):
            return value
        case _:
            return Unknown


@overload
def maybe_column_names(
    ctx: VisitorContext, expr: ast.List
) -> Generator[tuple[ast.expr, ColumnName], None, None]: ...
@overload
def maybe_column_names(
    ctx: VisitorContext, expr: list[ast.expr]
) -> Generator[tuple[ast.expr, ColumnName], None, None]: ...
@overload
def maybe_column_names(
    ctx: VisitorContext, expr: ast.expr
) -> Generator[tuple[ast.expr, ColumnName], None, None] | _Unknown: ...
def maybe_column_names(
    ctx: VisitorContext, expr: ast.expr | list[ast.expr]
) -> Generator[tuple[ast.expr, ColumnName], None, None] | _Unknown:
    match expr:
        case ast.List(elts):
            for elt in elts:
                column_name = maybe_column_name(ctx, elt)
                if isinstance(column_name, _Unknown):
                    continue
                yield elt, column_name
        case list():
            for ex in expr:
                column_name = maybe_column_name(ctx, ex)
                if isinstance(column_name, _Unknown):
                    continue
                yield ex, column_name
        case _:
            return Unknown
