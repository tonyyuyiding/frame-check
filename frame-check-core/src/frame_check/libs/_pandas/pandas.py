import ast
from typing import Generator

from frame_check.models import (
    is_column_name,
    Lib,
    VisitorContext,
    FrameClass,
    FrameInstance,
)
from frame_check.visitor import (
    get_argument,
    maybe_column_name,
    maybe_column_names,
)

from .._registry import func


@func(Lib.pd, "DataFrame")
def pd_DataFrame(ctx: VisitorContext, args: list[ast.expr], kwargs: list[ast.keyword]):
    data = get_argument(args, kwargs, pos=0, key="data")
    match data:
        case ast.Dict(keys, _):
            gen = maybe_column_names(ctx, [k for k in keys if k is not None])
            columns = set()
            for _, column_name in gen:
                columns.add(column_name)
            return FrameInstance(FrameClass.pd_DataFrame, columns, False)
        case ast.List(elts):
            columns = set()
            for elt in elts:
                if isinstance(elt, ast.Dict):
                    gen = maybe_column_names(
                        ctx, [k for k in elt.keys if k is not None]
                    )
                    for _, column_name in gen:
                        columns.add(column_name)
            return FrameInstance(FrameClass.pd_DataFrame, columns, False)
        case _:
            return FrameInstance(FrameClass.pd_DataFrame, set(), maybe_more=True)


@func(Lib.pd, "read_csv")
def pd_read_csv(ctx: VisitorContext, args: list[ast.expr], kwargs: list[ast.keyword]):
    usecols = get_argument(args, kwargs, key="usecols")
    if usecols is None:
        return FrameInstance(FrameClass.pd_DataFrame, set(), maybe_more=True)
    column_name = maybe_column_name(ctx, usecols)
    if is_column_name(column_name):
        return FrameInstance(FrameClass.pd_DataFrame, {column_name}, False)
    gen = maybe_column_names(ctx, usecols)
    if isinstance(gen, Generator):
        columns = set()
        for _, column_name in gen:
            columns.add(column_name)
        return FrameInstance(FrameClass.pd_DataFrame, columns, False)
    return FrameInstance(FrameClass.pd_DataFrame, set(), maybe_more=True)
