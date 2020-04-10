"""
Java Parser.
"""

from lark import Lark
from .common import CommonTransformer
from .package import PackageTransformer
from .imports import ImportTransformer
from .annotation import AnnotationTransformer
from .modifiers import ModifierTransformer
from .field import FieldTransformer
from .enum import EnumTransformer
from .method import MethodTransformer
from .clazz import ClassTransformer


class JavaTransformer(
    CommonTransformer,
    PackageTransformer,
    ImportTransformer,
    AnnotationTransformer,
    ModifierTransformer,
    FieldTransformer,
    EnumTransformer,
    MethodTransformer,
    ClassTransformer,
):
    pass


def create_parser(parser="earley"):
    return Lark.open(
        "java_parser/java.lark",
        parser=parser,
        propagate_positions=True,
        # transformer=JavaTransformer,
        start="clazz",
        debug=False,
    )
