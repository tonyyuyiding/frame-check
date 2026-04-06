import ast

from frame_check_core.models import FrameInstance, Unknown, VisitorContext, FCGenerator
from frame_check_core.libs import get_callable


def visit_Subscript(node: ast.Subscript, ctx: VisitorContext) -> FCGenerator:
    from . import visit

    # __setitem__ is handled by `visit_Assign`, so no need to worry here.
    value = yield from visit(node.value, ctx)
    if not isinstance(value, FrameInstance):
        return Unknown
    method = get_callable(value, "__getitem__")
    res = yield from method(ctx, [node.slice], [])
    return res
