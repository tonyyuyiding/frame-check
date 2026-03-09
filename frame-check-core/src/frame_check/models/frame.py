from collections.abc import Iterable

from .base import ColumnName, FrameClass


class FrameInstance:
    __slots__ = ("class_", "_columns", "maybe_more")
    class_: FrameClass
    _columns: set[ColumnName]
    maybe_more: bool

    def __init__(
        self, class_: FrameClass, columns: Iterable[ColumnName], maybe_more: bool
    ) -> None:
        self.class_ = class_
        self._columns = set(columns)
        self.maybe_more = maybe_more

    def has_column(self, column: ColumnName) -> bool:
        return column in self._columns

    def add_column(self, column: ColumnName) -> None:
        self._columns.add(column)

    def update_columns(self, columns: Iterable[ColumnName]) -> None:
        self._columns = set(columns)

    def copy(self) -> "FrameInstance":
        return FrameInstance(self.class_, self._columns, self.maybe_more)

    @property
    def columns(self) -> frozenset[ColumnName]:
        return frozenset(self._columns)
