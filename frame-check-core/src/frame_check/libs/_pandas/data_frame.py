import ast
from typing import Generator

from frame_check.models import (
    Diagnostic,
    VisitorContext,
    FrameClass,
    FrameInstance,
    Unknown,
)
from frame_check.visitor import get_argument, maybe_str, maybe_column_names

from .._registry import method


@method(FrameClass.pd_DataFrame, "__getitem__")
def pd_DataFrame_getitem(
    self: FrameInstance,
    ctx: VisitorContext,
    args: list[ast.expr],
    kwargs: list[ast.keyword],
):
    key = get_argument(args, kwargs, pos=0, key="key")
    if key is None:
        return Unknown
    column_name = maybe_str(ctx, key)
    if isinstance(column_name, str):
        if column_name not in self.columns:
            yield Diagnostic.mark_expr(key, self, column_name)
        return Unknown
    gen = maybe_column_names(ctx, key)
    if isinstance(gen, Generator):
        existing_columns = set()
        for expr, column_name in gen:
            if column_name in self.columns:
                existing_columns.add(column_name)
            else:
                yield Diagnostic.mark_expr(expr, self, column_name)
        return FrameInstance(self.class_, existing_columns, maybe_more=True)
    return Unknown


@method(FrameClass.pd_DataFrame, "__setitem__")
def pd_DataFrame_setitem(
    self: FrameInstance,
    ctx: VisitorContext,
    args: list[ast.expr],
    kwargs: list[ast.keyword],
):
    key = get_argument(args, kwargs, pos=0, key="key")
    if key is None:
        return Unknown
    column_name = maybe_str(ctx, key)
    if isinstance(column_name, str):
        new_frame = self.copy()
        new_frame.add_columns({column_name})
        return new_frame
    gen = maybe_column_names(ctx, key)
    if isinstance(gen, set):
        new_frame = self.copy()
        for _, column_name in gen:
            new_frame.add_column(column_name)
        return new_frame
    return Unknown


@method(FrameClass.pd_DataFrame, "assign")
def pd_DataFrame_assign(
    self: FrameInstance,
    ctx: VisitorContext,
    args: list[ast.expr],
    kwargs: list[ast.keyword],
):
    columns_assigned = (keyword.arg for keyword in kwargs if keyword.arg is not None)
    new_frame = self.copy()
    new_frame.add_columns(columns_assigned)
    return new_frame


@method(FrameClass.pd_DataFrame, "insert")
def pd_DataFrame_insert(
    self: FrameInstance,
    ctx: VisitorContext,
    args: list[ast.expr],
    kwargs: list[ast.keyword],
):
    column_arg = get_argument(args, kwargs, pos=1, key="column")
    if column_arg is None:
        return Unknown
    column_name = maybe_str(ctx, column_arg)
    if column_name is Unknown:
        return Unknown
    new_frame = self.copy()
    new_frame.add_columns({column_name})
    return new_frame
