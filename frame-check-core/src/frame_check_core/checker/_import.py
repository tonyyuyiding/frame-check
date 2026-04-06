import ast

from frame_check_core.models import FCValue, Lib, Unknown, VisitorContext


def visit_Import(node: ast.Import, ctx: VisitorContext) -> FCValue:
    for alias in node.names:
        try:
            lib = Lib(alias.name)
        except ValueError:
            continue
        asname = alias.asname or alias.name
        ctx.definitions[asname] = lib
    return Unknown
