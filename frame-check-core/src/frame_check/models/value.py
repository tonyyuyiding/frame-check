import ast
from collections.abc import Generator
from typing import Union

from .context import VisitorContext
from .diagnostic import Diagnostic
from .frame import FrameInstance


class _Unknown:
    pass


Unknown = _Unknown()

FCValue = Union[FrameInstance, "FCCallable", _Unknown]
FCGenerator = Generator[Diagnostic, None, FCValue]


class FCCallable:
    def __call__(
        self, context: VisitorContext, args: list[ast.expr], kwargs: list[ast.keyword]
    ) -> FCGenerator: ...
