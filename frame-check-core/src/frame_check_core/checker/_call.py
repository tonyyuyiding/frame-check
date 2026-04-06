import ast

from frame_check_core.models import (
    FrameInstance,
    Lib,
    Unknown,
    VisitorContext,
    FCGenerator,
)
from frame_check_core.libs import get_callable


def visit_Call(node: ast.Call, ctx: VisitorContext) -> FCGenerator:
    from . import visit

    match node.func:
        case ast.Attribute(value, attr):
            value = yield from visit(value, ctx)
            if not isinstance(value, (FrameInstance, Lib)):
                return Unknown
            func = get_callable(value, attr)
            res = yield from func(ctx, node.args, node.keywords)
            return res
        case _:
            return Unknown
