import unittest
from tests.helper import get_parser
from java_parser.enum import EnumTransformer
from java_parser.field import FieldTransformer
from java_parser.common import CommonTransformer
from java_parser.method import MethodTransformer
from java_parser.annotation import AnnotationTransformer


class TestEnumTransformer(
    CommonTransformer,
    MethodTransformer,
    AnnotationTransformer,
    FieldTransformer,
    EnumTransformer,
):
    pass


class TestEnum(unittest.TestCase):
    def test_enum_case1(self):

        text = "public enum EnumType {ENUM_1, ENUM_2, ENUM_3}"
        tree = get_parser("enum_field").parse(text)
        print(tree)
        result = TestEnumTransformer().transform(tree)
        print(result)
        expected = {
            "name": "EnumType",
            "body": [
                {"name": "ENUM_1", "type": "ENUM_ELEMENT", "lineno": 1, "linenoEnd": 1},
                {"name": "ENUM_2", "type": "ENUM_ELEMENT", "lineno": 1, "linenoEnd": 1},
                {"name": "ENUM_3", "type": "ENUM_ELEMENT", "lineno": 1, "linenoEnd": 1},
            ],
            "modifiers": ["public"],
            "type": "ENUM_FIELD",
            "lineno": 1,
            "linenoEnd": 1,
        }
        self.assertEqual(result, expected, "Not matched.")
