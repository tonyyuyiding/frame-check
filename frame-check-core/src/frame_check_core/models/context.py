from typing import Any


class VisitorContext:
    definitions: dict[str, Any]

    def __init__(self) -> None:
        self.definitions = {}
