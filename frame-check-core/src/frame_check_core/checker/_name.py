import ast

from frame_check_core.models import FCValue, Unknown, VisitorContext


def visit_Name(node: ast.Name, ctx: VisitorContext) -> FCValue:
    if node.id in ctx.definitions:
        return ctx.definitions[node.id]
    return Unknown
