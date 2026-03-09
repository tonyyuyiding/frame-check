import ast

from frame_check.models import FrameInstance, Unknown, VisitorContext, FCGenerator
from frame_check.libs import get_callable


def visit_Assign(ctx: VisitorContext, node: ast.Assign) -> FCGenerator:
    from . import visit

    value = yield from visit(ctx, node.value)
    if value is Unknown:
        return Unknown
    for target in node.targets:
        if isinstance(target, ast.Name) and value is not Unknown:
            ctx.definitions[target.id] = value

        elif isinstance(target, ast.Subscript):
            obj = yield from visit(ctx, target.value)
            if not isinstance(obj, FrameInstance):
                return Unknown
            method = get_callable(obj, "__setitem__")
            yield from method(ctx, [target.slice, node.value], [])
    return Unknown
