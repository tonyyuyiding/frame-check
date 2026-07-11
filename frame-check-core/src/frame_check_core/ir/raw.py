from abc import ABC
from dataclasses import dataclass
from typing import dataclass_transform

from libcst.metadata import CodeRange

from .common import BinOperator


@dataclass(slots=True, kw_only=True)
@dataclass_transform()
class _RawIRNode(ABC):
    code_range: CodeRange

    def __init_subclass__(cls, /, **kwargs):
        super().__init_subclass__(**kwargs)
        dataclass(cls, slots=True, kw_only=True)


class expr(_RawIRNode):
    pass


class stmt(_RawIRNode):
    pass


class Assign(stmt):
    targets: tuple[expr, ...]
    value: expr
    type_comment: str | None


class Attribute(expr):
    value: expr
    attr: str


class BinOp(expr):
    left: expr
    op: BinOperator
    right: expr


class CallKeyword(expr):
    arg: str | None
    value: expr


class Call(expr):
    func: expr
    args: tuple[expr, ...]
    keywords: tuple[CallKeyword, ...]


type _ConstantValue = str | bool | int | None


class Constant(expr):
    value: _ConstantValue


class Dict(expr):
    keys: tuple[expr | None, ...]
    values: tuple[expr, ...]


class ImportAlias(_RawIRNode):
    name: str
    asname: str | None


class Import(stmt):
    names: tuple[ImportAlias, ...]


class ImportFrom(stmt):
    module: str | None
    names: tuple[ImportAlias, ...]
    level: int


class List(expr):
    elts: tuple[expr, ...]


class Module(_RawIRNode):
    body: tuple[stmt, ...]


class Name(expr):
    id: str


class Unknown(expr):
    pass
