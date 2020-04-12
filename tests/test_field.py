import unittest
from tests.helper import get_parser
from java_parser.field import FieldTransformer
from java_parser.common import CommonTransformer
from java_parser.method import MethodTransformer
from java_parser.annotation import AnnotationTransformer


class CompoundFieldTransformer(
    CommonTransformer, MethodTransformer, AnnotationTransformer, FieldTransformer,
):
    pass


class TestField(unittest.TestCase):
    def test_field_case1(self):

        text = 'private static String name = "Real Name";'
        tree = get_parser("field").parse(text)
        print(tree)
        result = CompoundFieldTransformer().transform(tree)
        print(result)
        expected = {
            "classType": "String",
            "name": "name",
            "assign": '"Real Name"',
            "modifiers": ["private", "static"],
            "operator": "=",
            "type": "FIELD",
            "lineno": 1,
            "linenoEnd": 1,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_field_case2(self):

        text = "private final static String name;"
        tree = get_parser("field").parse(text)
        print(tree)
        result = CompoundFieldTransformer().transform(tree)
        print(result)
        expected = {
            "name": "name",
            "classType": "String",
            "modifiers": ["private", "final", "static"],
            "type": "FIELD",
            "lineno": 1,
            "linenoEnd": 1,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_field_case3(self):

        text = "int[] name;"
        tree = get_parser("field").parse(text)
        print(tree)
        result = CompoundFieldTransformer().transform(tree)
        print(result)
        expected = {
            "classType": {"name": "int", "arraySuffix": "[]"},
            "name": "name",
            "type": "FIELD",
            "lineno": 1,
            "linenoEnd": 1,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_field_case4(self):

        text = 'private static final String SOME_CONSTANT = "SOME_CONSTANT";'
        tree = get_parser("field").parse(text)
        print(tree)
        result = CompoundFieldTransformer().transform(tree)
        print(result)
        expected = {
            "classType": "String",
            "name": "SOME_CONSTANT",
            "assign": '"SOME_CONSTANT"',
            "modifiers": ["private", "static", "final"],
            "operator": "=",
            "type": "FIELD",
            "lineno": 1,
            "linenoEnd": 1,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_field_case5(self):

        text = "private int number = 12345;"
        tree = get_parser("field").parse(text)
        print(tree)
        result = CompoundFieldTransformer().transform(tree)
        print(result)
        expected = {
            "classType": "int",
            "name": "number",
            "assign": 12345,
            "modifiers": ["private"],
            "operator": "=",
            "type": "FIELD",
            "lineno": 1,
            "linenoEnd": 1,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_field_case6(self):

        text = "protected Map<String, String> map = new HashMap<>();"
        tree = get_parser("field").parse(text)
        print(tree)
        result = CompoundFieldTransformer().transform(tree)
        print(result)
        expected = {
            "classType": {"name": "Map", "generic": ["String", "String"]},
            "name": "map",
            "assign": {
                "value": {
                    "name": {"name": "HashMap", "generic": ["<>"]},
                    "type": "INVOCATION",
                },
                "type": "NEW_EXPRESSION",
            },
            "modifiers": ["protected"],
            "operator": "=",
            "type": "FIELD",
            "lineno": 1,
            "linenoEnd": 1,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_field_case7(self):

        text = "private StringBuilder sb;"
        tree = get_parser("field").parse(text)
        print(tree)
        result = CompoundFieldTransformer().transform(tree)
        print(result)
        expected = {
            "classType": "StringBuilder",
            "name": "sb",
            "modifiers": ["private"],
            "type": "FIELD",
            "lineno": 1,
            "linenoEnd": 1,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_field_case8(self):

        text = "public boolean flag = false;"
        tree = get_parser("field").parse(text)
        print(tree)
        result = CompoundFieldTransformer().transform(tree)
        print(result)
        expected = {
            "classType": "boolean",
            "name": "flag",
            "assign": False,
            "modifiers": ["public"],
            "operator": "=",
            "type": "FIELD",
            "lineno": 1,
            "linenoEnd": 1,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_field_case9(self):

        text = "boolean flag = false;"
        tree = get_parser("field").parse(text)
        print(tree)
        result = CompoundFieldTransformer().transform(tree)
        print(result)
        expected = {
            "classType": "boolean",
            "name": "flag",
            "assign": False,
            "operator": "=",
            "type": "FIELD",
            "lineno": 1,
            "linenoEnd": 1,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_field_case10(self):

        text = """private static final String SQL_TEXT = " AND NOT EXISTS ("
            + "SELECT * FROM TBL ABC WHERE ABC.COL_NAME=DBC.ABCD AND ABC.FLG='0') ";"""
        tree = get_parser("field").parse(text)
        print(tree)
        result = CompoundFieldTransformer().transform(tree)
        print(result)
        expected = {
            "classType": "String",
            "name": "SQL_TEXT",
            "assign": {
                "left": '" AND NOT EXISTS ("',
                "chain": [
                    {
                        "value": "\"SELECT * FROM TBL ABC WHERE ABC.COL_NAME=DBC.ABCD AND ABC.FLG='0') \"",
                        "operator": "+",
                    }
                ],
                "type": "ARITHMETIC_EXPRESSION",
            },
            "modifiers": ["private", "static", "final"],
            "operator": "=",
            "type": "FIELD",
            "lineno": 1,
            "linenoEnd": 2,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_field_case11(self):

        text = """private static final String SQL_TEXT = " AND NOT EXISTS ("
            + "SELECT * FROM TBL ABC WHERE ABC.COL_NAME=DBC.ABCD AND ABC.FLG='0') ";
            private static final String SQL_TEXT2 = " AND NOT EXISTS ("
            + "SELECT * FROM TBL ABC WHERE ABC.COL_NAME=DBC.ABCD AND ABC.FLG='0') ";"""
        tree = get_parser("fields").parse(text)
        print(tree)
        result = CompoundFieldTransformer().transform(tree)
        print(result)
        expected = [
            {
                "classType": "String",
                "name": "SQL_TEXT",
                "assign": {
                    "left": '" AND NOT EXISTS ("',
                    "chain": [
                        {
                            "value": "\"SELECT * FROM TBL ABC WHERE ABC.COL_NAME=DBC.ABCD AND ABC.FLG='0') \"",
                            "operator": "+",
                        }
                    ],
                    "type": "ARITHMETIC_EXPRESSION",
                },
                "modifiers": ["private", "static", "final"],
                "operator": "=",
                "type": "FIELD",
                "lineno": 1,
                "linenoEnd": 2,
            },
            {
                "classType": "String",
                "name": "SQL_TEXT2",
                "assign": {
                    "left": '" AND NOT EXISTS ("',
                    "chain": [
                        {
                            "value": "\"SELECT * FROM TBL ABC WHERE ABC.COL_NAME=DBC.ABCD AND ABC.FLG='0') \"",
                            "operator": "+",
                        }
                    ],
                    "type": "ARITHMETIC_EXPRESSION",
                },
                "modifiers": ["private", "static", "final"],
                "operator": "=",
                "type": "FIELD",
                "lineno": 3,
                "linenoEnd": 4,
            },
        ]
        self.assertEqual(result, expected, "Not matched.")

    def test_field_case12(self):

        text = """@Annotation
        @Another(Some, Values, Here)
        boolean flag = false;"""
        tree = get_parser("fields").parse(text)
        print(tree)
        result = CompoundFieldTransformer().transform(tree)
        print(result)
        expected = [
            {
                "classType": "boolean",
                "name": "flag",
                "assign": False,
                "annotations": [
                    {
                        "name": "Annotation",
                        "lineno": 1,
                        "linenoEnd": 1,
                        "type": "ANNOTATION",
                    },
                    {
                        "name": "Another",
                        "lineno": 2,
                        "linenoEnd": 2,
                        "type": "ANNOTATION",
                        "args": ["Some", "Values", "Here"],
                    },
                ],
                "operator": "=",
                "type": "FIELD",
                "lineno": 1,
                "linenoEnd": 3,
            }
        ]
        self.assertEqual(result, expected, "Not matched.")

    def test_field_case13(self):

        text = """
        /**
        * Test Comment.
        * End.
        */
        @Annotation
        @Another(Some, Values, Here)
        boolean flag = false;"""
        tree = get_parser("fields").parse(text)
        print(tree)
        result = CompoundFieldTransformer().transform(tree)
        print(result)
        expected = [
            {
                "classType": "boolean",
                "name": "flag",
                "assign": False,
                "annotations": [
                    {
                        "name": "Annotation",
                        "lineno": 6,
                        "linenoEnd": 6,
                        "type": "ANNOTATION",
                    },
                    {
                        "name": "Another",
                        "lineno": 7,
                        "linenoEnd": 7,
                        "type": "ANNOTATION",
                        "args": ["Some", "Values", "Here"],
                    },
                ],
                "comment": ["/**", "* Test Comment.", "* End.", "*/"],
                "operator": "=",
                "type": "FIELD",
                "lineno": 2,
                "linenoEnd": 8,
            }
        ]
        self.assertEqual(result, expected, "Not matched.")
