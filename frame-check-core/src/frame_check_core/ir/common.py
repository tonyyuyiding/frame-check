from enum import Enum


class BinOperator(Enum):
    ADD = "+"
    SUBTRACT = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    FLOOR_DIVIDE = "//"
    MODULO = "%"
    POWER = "**"
    LEFT_SHIFT = "<<"
    RIGHT_SHIFT = ">>"
    BIT_OR = "|"
    BIT_AND = "&"
    BIT_XOR = "^"
    MATRIX_MULTIPLY = "@"
