import ast

from ..models import FCValue, Lib, Unknown, VisitorContext


def visit_Import(ctx: VisitorContext, node: ast.Import) -> FCValue:
    for alias in node.names:
        if alias.name in Lib:
            asname = alias.asname or alias.name
            ctx.definitions[asname] = Lib[alias.name]
    return Unknown
