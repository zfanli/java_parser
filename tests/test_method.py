import unittest
from tests.helper import get_parser
from java_parser.method import MethodTransformer
from java_parser.common import CommonTransformer
from java_parser.modifiers import ModifierTransformer


class TestMethodTransformer(CommonTransformer, ModifierTransformer, MethodTransformer):
    pass


class TestMethod(unittest.TestCase):
    def test_stmt_case1(self):

        text = "break;"
        tree = get_parser("simple_stmt").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {"name": "break", "type": "BREAK", "lineno": 1, "linenoEnd": 1}
        self.assertEqual(result, expected, "Not matched.")

    def test_stmt_case2(self):

        text = "continue;"
        tree = get_parser("simple_stmt").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {"name": "continue", "type": "CONTINUE", "lineno": 1, "linenoEnd": 1}
        self.assertEqual(result, expected, "Not matched.")

    def test_stmt_case3(self):

        text = "return;"
        tree = get_parser("simple_stmt").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {"name": "return", "type": "RETURN", "lineno": 1, "linenoEnd": 1}
        self.assertEqual(result, expected, "Not matched.")

    def test_stmt_case4(self):

        text = "return something(args);"
        tree = get_parser("simple_stmt").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {
            "name": "return",
            "type": "RETURN",
            "lineno": 1,
            "linenoEnd": 1,
            "value": {"name": "something", "type": "INVOCATION", "args": ["args"]},
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_stmt_case5(self):

        text = 'throw new Exception("Something went wrong");'
        tree = get_parser("simple_stmt").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {
            "name": "throw",
            "type": "THROW",
            "lineno": 1,
            "linenoEnd": 1,
            "value": {
                "value": {
                    "name": "Exception",
                    "type": "INVOCATION",
                    "args": ['"Something went wrong"'],
                },
                "type": "NEW_EXPRESSION",
            },
        }
        self.assertEqual(result, expected, "Not matched.")
