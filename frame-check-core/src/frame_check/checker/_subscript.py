import ast

from frame_check.models import FrameInstance, Unknown, VisitorContext, FCGenerator
from frame_check.libs import get_callable


def visit_Subscript(ctx: VisitorContext, node: ast.Subscript) -> FCGenerator:
    from . import visit

    # __setitem__ is handled by `visit_Assign`, so no need to worry here.
    value = yield from visit(ctx, node.value)
    if not isinstance(value, FrameInstance):
        return Unknown
    method = get_callable(value, "__getitem__")
    res = yield from method(ctx, [node.slice], [])
    return res
