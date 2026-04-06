import ast

from frame_check_core.models import FrameInstance, Unknown, VisitorContext, FCGenerator
from frame_check_core.libs import get_callable

from .marks import mark_setitem


def visit_Assign(node: ast.Assign, ctx: VisitorContext) -> FCGenerator:
    from .visit import visit

    value = yield from visit(node.value, ctx)
    for target in node.targets:
        if isinstance(target, ast.Name) and value is not Unknown:
            ctx.definitions[target.id] = value

        elif isinstance(target, ast.Subscript):
            mark_setitem(target)
            obj = yield from visit(target.value, ctx)
            if not isinstance(obj, FrameInstance):
                return Unknown
            method = get_callable(obj, "__setitem__")
            yield from method(ctx, [target.slice, node.value], [])
    return Unknown
