import ast
from collections.abc import Callable, Generator
from typing import Union

from .context import VisitorContext
from .diagnostic import Diagnostic
from .frame import FrameInstance


class _Unknown:
    pass


Unknown = _Unknown()

FCValue = Union[FrameInstance, "FCCallable", _Unknown]
FCGenerator = Generator[Diagnostic, None, FCValue]
FCCallableInit = Callable[
    [VisitorContext, list[ast.expr], list[ast.keyword]], FCGenerator | FCValue
]


class FCCallable:
    def __init__(self, func: FCCallableInit) -> None:
        self.func = func

    def __call__(
        self,
        context: VisitorContext,
        args: list[ast.expr],
        kwargs: list[ast.keyword],
    ) -> FCGenerator:
        res = self.func(context, args, kwargs)
        if isinstance(res, Generator):
            res = yield from res
            return res
        else:
            return res

    @staticmethod
    def empty() -> "FCCallable":
        return FCCallable(lambda ctx, args, kwargs: Unknown)
