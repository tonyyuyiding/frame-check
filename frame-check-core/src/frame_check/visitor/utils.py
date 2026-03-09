import ast


def get_argument(
    args: list[ast.expr],
    keywords: list[ast.keyword],
    *,
    pos: int | None = None,
    key: str | None = None,
) -> ast.expr | None:
    if pos is not None and pos < len(args):
        return args[pos]
    if key is not None:
        for keyword in keywords:
            if keyword.arg == key:
                return keyword.value
    return None
