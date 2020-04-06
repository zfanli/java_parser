"""
Helper.
"""

from lark import Lark


def get_parser(start):

    return Lark.open(
        "java_parser/java.lark",
        parser="lalr",
        propagate_positions=True,
        start=start,
        debug=True,
    )
