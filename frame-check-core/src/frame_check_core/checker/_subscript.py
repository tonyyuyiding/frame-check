import ast

from frame_check_core.models import FrameInstance, Unknown, VisitorContext, FCGenerator
from frame_check_core.libs import get_callable

from .marks import is_setitem


def visit_Subscript(node: ast.Subscript, ctx: VisitorContext) -> FCGenerator:
    from .visit import visit

    if is_setitem(node):
        # __setitem__ is handled by `visit_Assign`
        return Unknown
    value = yield from visit(node.value, ctx)
    if not isinstance(value, FrameInstance):
        return Unknown
    method = get_callable(value, "__getitem__")
    res = yield from method(ctx, [node.slice], [])
    return res
