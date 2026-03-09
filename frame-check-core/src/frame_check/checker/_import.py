import ast

from ..models import FCValue, Lib, Unknown, VisitorContext


def visit_Import(ctx: VisitorContext, node: ast.Import) -> FCValue:
    for alias in node.names:
        try:
            lib = Lib(alias.name)
        except ValueError:
            continue
        asname = alias.asname or alias.name
        ctx.definitions[asname] = lib
    return Unknown
