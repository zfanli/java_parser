import unittest
from tests.helper import get_parser
from java_parser.common import CommonTransformer


class TestModifiersTransformer(CommonTransformer):
    pass


class TestModifiers(unittest.TestCase):
    def test_modifier_case1(self):

        text = "private public default protected"
        tree = get_parser("modifiers").parse(text)
        print(tree)
        result = TestModifiersTransformer().transform(tree)
        print(result)
        expected = ["private", "public", "default", "protected"]
        self.assertEqual(result, expected, "Not matched.")

    def test_modifier_case2(self):

        text = """
        // Test comment
        final
        static
        transient
        synchronized
        volatile
        abstract
        """
        tree = get_parser("modifiers").parse(text)
        print(tree)
        result = TestModifiersTransformer().transform(tree)
        print(result)
        expected = [
            "final",
            "static",
            "transient",
            "synchronized",
            "volatile",
            "abstract",
        ]
        self.assertEqual(result, expected, "Not matched.")
