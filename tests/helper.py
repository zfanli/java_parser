"""
Helper.
"""

from lark import Lark


def get_parser(start, parser="earley"):

    return Lark.open(
        "java_parser/java.lark",
        parser=parser,
        propagate_positions=True,
        start=start,
        debug=True,
        # ambiguity="explicit",
    )
