import unittest
from tests.helper import get_parser
from java_parser.modifiers import ModifiersTransformer


class TestModifiers(unittest.TestCase):
    def test_modifier_case1(self):

        text = "private public default protected"
        tree = get_parser("modifiers").parse(text)
        print(tree)
        result = ModifiersTransformer().transform(tree)
        print(result)
        expected = {
            "modifiers": ["private", "public", "default", "protected"],
            "lineno": 1,
            "linenoEnd": 1,
        }
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
        result = ModifiersTransformer().transform(tree)
        print(result)
        expected = {
            "modifiers": [
                "final",
                "static",
                "transient",
                "synchronized",
                "volatile",
                "abstract",
            ],
            "lineno": 3,
            "linenoEnd": 8,
        }
        self.assertEqual(result, expected, "Not matched.")
