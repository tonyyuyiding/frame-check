import ast

from ..models import FCValue, Unknown, VisitorContext


def visit_Name(ctx: VisitorContext, node: ast.Name) -> FCValue:
    if node.id in ctx.definitions:
        return ctx.definitions[node.id]
    return Unknown
