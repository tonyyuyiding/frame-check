from abc import ABC
from dataclasses import dataclass
from typing import dataclass_transform

from libcst.metadata import CodeRange

from .common import BinOperator


@dataclass
@dataclass_transform()
class _RawIRNode(ABC):
    code_range: CodeRange | None

    def __init_subclass__(cls, /, **kwargs):
        super().__init_subclass__(**kwargs)
        if issubclass(cls, ABC):
            dataclass(cls)
        else:
            dataclass(cls, slots=True, kw_only=True)


class expr(_RawIRNode, ABC):
    pass


class stmt(_RawIRNode, ABC):
    pass


class Assign(stmt):
    targets: tuple[expr, ...]
    value: expr
    type_comment: str | None

    def __str__(self) -> str:
        targets = " = ".join(str(t) for t in self.targets)
        return f"{targets} = {self.value}"


class Attribute(expr):
    value: expr
    attr: str

    def __str__(self) -> str:
        return f"{self.value}.{self.attr}"


class BinOp(expr):
    left: expr
    op: BinOperator
    right: expr

    def __str__(self) -> str:
        return f"({self.left} {self.op.value} {self.right})"


class CallKeyword(expr):
    arg: str | None
    value: expr

    def __str__(self) -> str:
        if self.arg is None:
            return str(self.value)
        return f"{self.arg}={self.value}"


class Call(expr):
    func: expr
    args: tuple[expr, ...]
    keywords: tuple[CallKeyword, ...]

    def __str__(self) -> str:
        parts = [str(a) for a in self.args]
        parts.extend(str(k) for k in self.keywords)
        return f"{self.func}({', '.join(parts)})"


type _ConstantValue = str | bool | int | None


class Constant(expr):
    value: _ConstantValue

    def __str__(self) -> str:
        return repr(self.value)


class Dict(expr):
    keys: tuple[expr | None, ...]
    values: tuple[expr, ...]

    def __str__(self) -> str:
        pairs = (
            f"{k}: {v}" if k is not None else f"**{v}"
            for k, v in zip(self.keys, self.values, strict=True)
        )
        return f"{{{', '.join(pairs)}}}"


class Expr(stmt):
    value: expr

    def __str__(self) -> str:
        return str(self.value)


class ImportAlias(_RawIRNode):
    name: str
    asname: str | None

    def __str__(self) -> str:
        if self.asname is None:
            return self.name
        return f"{self.name} as {self.asname}"


class Import(stmt):
    names: tuple[ImportAlias, ...]

    def __str__(self) -> str:
        return f"import {', '.join(str(n) for n in self.names)}"


class ImportFrom(stmt):
    module: str | None
    names: tuple[ImportAlias, ...]
    level: int

    def __str__(self) -> str:
        dots = "." * self.level
        mod = self.module or ""
        names = ", ".join(str(n) for n in self.names)
        return f"from {dots}{mod} import {names}"


class List(expr):
    elts: tuple[expr, ...]

    def __str__(self) -> str:
        return f"[{', '.join(str(e) for e in self.elts)}]"


class Module(_RawIRNode):
    body: tuple[stmt, ...]

    def __str__(self) -> str:
        return "\n".join(str(s) for s in self.body)


class Name(expr):
    id: str

    def __str__(self) -> str:
        return self.id


class Unknown(expr):
    def __str__(self) -> str:
        return "<?>"
