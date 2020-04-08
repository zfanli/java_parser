import unittest
from tests.helper import get_parser
from java_parser.common import CommonTransformer


class TestCommon(unittest.TestCase):
    def test_class_type_case1(self):

        text = "HashMap<String, Object>"
        tree = get_parser("class_type").parse(text)
        print(tree)
        result = CommonTransformer().transform(tree)
        print(result)
        expected = {"name": "HashMap", "generic": ["String", "Object"]}
        self.assertEqual(result, expected, "Not matched.")

    def test_class_type_case2(self):

        text = "String"
        tree = get_parser("class_type").parse(text)
        print(tree)
        result = CommonTransformer().transform(tree)
        print(result)
        expected = "String"
        self.assertEqual(result, expected, "Not matched.")

    def test_class_type_case3(self):

        text = "List<>"
        tree = get_parser("class_type").parse(text)
        print(tree)
        result = CommonTransformer().transform(tree)
        print(result)
        expected = {"name": "List", "generic": ["<>"]}
        self.assertEqual(result, expected, "Not matched.")

    def test_class_type_case4(self):

        text = "HashMap<String, Map<String, Object>>"
        tree = get_parser("class_type").parse(text)
        print(tree)
        result = CommonTransformer().transform(tree)
        print(result)
        expected = {
            "name": "HashMap",
            "generic": ["String", {"name": "Map", "generic": ["String", "Object"]}],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_class_type_case5(self):

        text = "HashMap<>"
        tree = get_parser("class_type").parse(text)
        print(tree)
        result = CommonTransformer().transform(tree)
        print(result)
        expected = {"name": "HashMap", "generic": ["<>"]}
        self.assertEqual(result, expected, "Not matched.")

    def test_cast_type_case1(self):

        text = "(String)"
        tree = get_parser("cast_type").parse(text)
        print(tree)
        result = CommonTransformer().transform(tree)
        print(result)
        expected = "String"
        self.assertEqual(result, expected, "Not matched.")

    def test_cast_type_case2(self):

        text = "(Map<String, Object>)"
        tree = get_parser("cast_type").parse(text)
        print(tree)
        result = CommonTransformer().transform(tree)
        print(result)
        expected = {"name": "Map", "generic": ["String", "Object"]}
        self.assertEqual(result, expected, "Not matched.")

    def test_primary_case1(self):

        text = '"(Map<String, Object>)"'
        tree = get_parser("primary").parse(text)
        print(tree)
        result = CommonTransformer().transform(tree)
        print(result)
        expected = '"(Map<String, Object>)"'
        self.assertEqual(result, expected, "Not matched.")

    def test_primary_case2(self):

        text = "true"
        tree = get_parser("primary").parse(text)
        print(tree)
        result = CommonTransformer().transform(tree)
        print(result)
        expected = True
        self.assertEqual(result, expected, "Not matched.")

    def test_primary_case3(self):

        text = "false"
        tree = get_parser("primary").parse(text)
        print(tree)
        result = CommonTransformer().transform(tree)
        print(result)
        expected = False
        self.assertEqual(result, expected, "Not matched.")

    def test_primary_case4(self):

        text = "null"
        tree = get_parser("primary").parse(text)
        print(tree)
        result = CommonTransformer().transform(tree)
        print(result)
        expected = None
        self.assertEqual(result, expected, "Not matched.")

    def test_primary_case5(self):

        text = "123.456"
        tree = get_parser("primary").parse(text)
        print(tree)
        result = CommonTransformer().transform(tree)
        print(result)
        expected = 123.456
        self.assertEqual(result, expected, "Not matched.")

    def test_primary_case6(self):

        text = "-5896.214"
        tree = get_parser("primary").parse(text)
        print(tree)
        result = CommonTransformer().transform(tree)
        print(result)
        expected = -5896.214
        self.assertEqual(result, expected, "Not matched.")

    def test_primary_case7(self):

        text = "999"
        tree = get_parser("primary").parse(text)
        print(tree)
        result = CommonTransformer().transform(tree)
        print(result)
        expected = 999
        self.assertEqual(result, expected, "Not matched.")

    def test_comment_case1(self):

        text = """
        /**
        * Test comment
        * Comment end.
        */
        """
        tree = get_parser("comment").parse(text)
        print(tree)
        result = CommonTransformer().transform(tree)
        print(result)
        expected = ["/**", "* Test comment", "* Comment end.", "*/"]
        self.assertEqual(result, expected, "Not matched.")

    def test_comment_case2(self):

        text = """
        /**
         Test comment
         Comment end.
        */
        """
        tree = get_parser("comment").parse(text)
        print(tree)
        result = CommonTransformer().transform(tree)
        print(result)
        expected = ["/**", "Test comment", "Comment end.", "*/"]
        self.assertEqual(result, expected, "Not matched.")

    def test_comment_case3(self):

        text = """
        /*
         Test comment
         Comment end.
        */
        """
        tree = get_parser("comment").parse(text)
        print(tree)
        result = CommonTransformer().transform(tree)
        print(result)
        expected = ["/*", "Test comment", "Comment end.", "*/"]
        self.assertEqual(result, expected, "Not matched.")

    def test_arguments_case1(self):

        text = "test ? ok : ng, abc.arg2(test, arg3), item[0], name.attribute"
        tree = get_parser("arguments").parse(text)
        print(tree)
        result = CommonTransformer().transform(tree)
        print(result)
        expected = [
            {
                "condition": "test",
                "ifTrue": "ok",
                "ifFalse": "ng",
                "type": "TERNARY_EXPRESSION",
            },
            {"name": "abc.arg2", "args": ["test", "arg3"], "type": "INVOCATION"},
            "item[0]",
            "name.attribute",
        ]
        self.assertEqual(result, expected, "Not matched.")

    def test_arguments_case2(self):

        text = "con1 && !con2 || con3 ? ok : ng"
        tree = get_parser("arguments").parse(text)
        print(tree)
        result = CommonTransformer().transform(tree)
        print(result)
        expected = [
            {
                "condition": {
                    "left": {
                        "left": "con1",
                        "right": [{"value": "con2", "type": "TEST_NOT"}],
                        "type": "TEST_AND",
                    },
                    "right": ["con3"],
                    "type": "TEST_OR",
                },
                "ifTrue": "ok",
                "ifFalse": "ng",
                "type": "TERNARY_EXPRESSION",
            }
        ]
        self.assertEqual(result, expected, "Not matched.")

    def test_arguments_case3(self):

        text = "con1 > con2 || con3 == con4 && con5 != con6 || con7 <= con8"
        tree = get_parser("arguments").parse(text)
        print(tree)
        result = CommonTransformer().transform(tree)
        print(result)
        expected = [
            {
                "left": {
                    "left": "con1",
                    "chain": [{"value": "con2", "operator": ">"}],
                    "type": "COMPARISON",
                },
                "right": [
                    {
                        "left": {
                            "left": "con3",
                            "chain": [{"value": "con4", "operator": "=="}],
                            "type": "COMPARISON",
                        },
                        "right": [
                            {
                                "left": "con5",
                                "chain": [{"value": "con6", "operator": "!="}],
                                "type": "COMPARISON",
                            }
                        ],
                        "type": "TEST_AND",
                    },
                    {
                        "left": "con7",
                        "chain": [{"value": "con8", "operator": "<="}],
                        "type": "COMPARISON",
                    },
                ],
                "type": "TEST_OR",
            }
        ]
        self.assertEqual(result, expected, "Not matched.")

    def test_arguments_case4(self):

        text = "con1 ^ con2 ^ con3"
        tree = get_parser("arguments").parse(text)
        print(tree)
        result = CommonTransformer().transform(tree)
        print(result)
        expected = [{"value": ["con1", "con2", "con3"], "type": "XOR_EXPRESSION"}]
        self.assertEqual(result, expected, "Not matched.")

    def test_arguments_case5(self):

        text = "con1 ^ con2 ^ con3 | con4 | con5 | con6 & con7 & con8"
        tree = get_parser("arguments").parse(text)
        print(tree)
        result = CommonTransformer().transform(tree)
        print(result)
        expected = [
            {
                "value": [
                    {"value": ["con1", "con2", "con3"], "type": "XOR_EXPRESSION"},
                    "con4",
                    "con5",
                    {"value": ["con6", "con7", "con8"], "type": "BITWISE_AND"},
                ],
                "type": "BITWISE_OR",
            }
        ]
        self.assertEqual(result, expected, "Not matched.")

    def test_arguments_case6(self):

        text = "var1 + var2 > var3"
        tree = get_parser("arguments").parse(text)
        print(tree)
        result = CommonTransformer().transform(tree)
        print(result)
        expected = [
            {
                "left": {
                    "left": "var1",
                    "chain": [{"value": "var2", "operator": "+"}],
                    "type": "ARITHMETIC_EXPRESSION",
                },
                "chain": [{"value": "var3", "operator": ">"}],
                "type": "COMPARISON",
            }
        ]
        self.assertEqual(result, expected, "Not matched.")

    def test_arguments_case7(self):

        text = "var1 + var2 - var3 * var4 / var5"
        tree = get_parser("arguments").parse(text)
        print(tree)
        result = CommonTransformer().transform(tree)
        print(result)
        expected = [
            {
                "left": "var1",
                "chain": [
                    {"value": "var2", "operator": "+"},
                    {
                        "value": {
                            "left": "var3",
                            "chain": [
                                {"value": "var4", "operator": "*"},
                                {"value": "var5", "operator": "/"},
                            ],
                            "type": "ARITHMETIC_EXPRESSION",
                        },
                        "operator": "-",
                    },
                ],
                "type": "ARITHMETIC_EXPRESSION",
            }
        ]
        self.assertEqual(result, expected, "Not matched.")

    def test_arguments_case8(self):

        text = "var ** 2"
        tree = get_parser("arguments").parse(text)
        print(tree)
        result = CommonTransformer().transform(tree)
        print(result)
        expected = [{"value": "var", "power": 2, "type": "POWER_EXPRESSION"}]
        self.assertEqual(result, expected, "Not matched.")

    def test_arguments_case9(self):

        text = "var1 << var2 >> var3"
        tree = get_parser("arguments").parse(text)
        print(tree)
        result = CommonTransformer().transform(tree)
        print(result)
        expected = [
            {
                "left": "var1",
                "chain": [
                    {"value": "var2", "operator": "<<"},
                    {"value": "var3", "operator": ">>"},
                ],
                "type": "SHIFT_EXPRESSION",
            }
        ]
        self.assertEqual(result, expected, "Not matched.")

    def test_arguments_case10(self):

        text = "(Map<Object, Object>) new HashMap<String, Object>()"
        tree = get_parser("arguments").parse(text)
        print(tree)
        result = CommonTransformer().transform(tree)
        print(result)
        expected = [
            {
                "value": {
                    "value": {
                        "name": {"name": "HashMap", "generic": ["String", "Object"]},
                        "type": "INVOCATION",
                    },
                    "type": "NEW_EXPRESSION",
                },
                "cast": {"name": "Map", "generic": ["Object", "Object"]},
                "type": "CAST_EXPRESSION",
            }
        ]
        self.assertEqual(result, expected, "Not matched.")

    def test_arguments_case11(self):

        text = "SomeClass.<GenericType> getBody().attribute"
        tree = get_parser("arguments").parse(text)
        print(tree)
        result = CommonTransformer().transform(tree)
        print(result)
        expected = [
            {
                "base": {
                    "name": "SomeClass.<GenericType> getBody",
                    "type": "INVOCATION",
                },
                "name": "attribute",
                "type": "ATTRIBUTE",
            }
        ]
        self.assertEqual(result, expected, "Not matched.")

    def test_arguments_case12(self):

        text = "new String[0]"
        tree = get_parser("arguments").parse(text)
        print(tree)
        result = CommonTransformer().transform(tree)
        print(result)
        expected = [{"value": "String[0]", "type": "NEW_EXPRESSION"}]
        self.assertEqual(result, expected, "Not matched.")

    def test_arguments_case13(self):

        text = "name = value"
        tree = get_parser("arguments").parse(text)
        print(tree)
        result = CommonTransformer().transform(tree)
        print(result)
        expected = [{"key": "name", "value": "value", "type": "KEY_VALUE_PAIR"}]
        self.assertEqual(result, expected, "Not matched.")

    def test_arguments_case14(self):

        text = "int[]"
        tree = get_parser("arguments").parse(text)
        print(tree)
        result = CommonTransformer().transform(tree)
        print(result)
        expected = [{"name": "int", "arraySuffix": "[]"}]
        self.assertEqual(result, expected, "Not matched.")

    def test_parameters_case1(self):

        text = "Object... args"
        tree = get_parser("parameter").parse(text)
        print(tree)
        result = CommonTransformer().transform(tree)
        print(result)
        expected = {"name": "args", "classType": "Object...", "type": "PARAMETER"}
        self.assertEqual(result, expected, "Not matched.")

    def test_parameters_case1(self):

        text = "Map<String, Map<String, String>> map"
        tree = get_parser("parameter").parse(text)
        print(tree)
        result = CommonTransformer().transform(tree)
        print(result)
        expected = {
            "name": "map",
            "classType": {
                "name": "Map",
                "generic": ["String", {"name": "Map", "generic": ["String", "String"]}],
            },
            "type": "PARAMETER",
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_test_case1(self):

        text = "new HashMap<>()"
        tree = get_parser("test").parse(text)
        print(tree)
        result = CommonTransformer().transform(tree)
        print(result)
        expected = {
            "value": {
                "name": {"name": "HashMap", "generic": ["<>"]},
                "type": "INVOCATION",
            },
            "type": "NEW_EXPRESSION",
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_test_case2(self):

        text = "CallableName(recursion(), another(someValues, last))"
        tree = get_parser("test").parse(text)
        print(tree)
        result = CommonTransformer().transform(tree)
        print(result)
        expected = {
            "name": "CallableName",
            "type": "INVOCATION",
            "args": [
                {"name": "recursion", "type": "INVOCATION"},
                {
                    "name": "another",
                    "type": "INVOCATION",
                    "args": ["someValues", "last"],
                },
            ],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_test_case3(self):

        text = "CallableName.attribute(recursion(), another(someValues, last))"
        tree = get_parser("test").parse(text)
        print(tree)
        result = CommonTransformer().transform(tree)
        print(result)
        expected = {
            "name": "CallableName.attribute",
            "type": "INVOCATION",
            "args": [
                {"name": "recursion", "type": "INVOCATION"},
                {
                    "name": "another",
                    "type": "INVOCATION",
                    "args": ["someValues", "last"],
                },
            ],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_test_case4(self):

        text = "target.<Generic> doThat().doThis()"
        tree = get_parser("test").parse(text)
        print(tree)
        result = CommonTransformer().transform(tree)
        print(result)
        expected = {
            "name": {
                "base": {"name": "target.<Generic> doThat", "type": "INVOCATION"},
                "name": "doThis",
                "type": "ATTRIBUTE",
            },
            "type": "INVOCATION",
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_test_case5(self):

        text = "object.getSomething(new Something())"
        tree = get_parser("test").parse(text)
        print(tree)
        result = CommonTransformer().transform(tree)
        print(result)
        expected = {
            "name": "object.getSomething",
            "type": "INVOCATION",
            "args": [
                {
                    "value": {"name": "Something", "type": "INVOCATION"},
                    "type": "NEW_EXPRESSION",
                }
            ],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_test_case6(self):

        text = "array[1].name()"
        tree = get_parser("test").parse(text)
        print(tree)
        result = CommonTransformer().transform(tree)
        print(result)
        expected = {"name": "array[1].name", "type": "INVOCATION"}
        self.assertEqual(result, expected, "Not matched.")

    def test_test_case7(self):

        text = "!condition"
        tree = get_parser("test").parse(text)
        print(tree)
        result = CommonTransformer().transform(tree)
        print(result)
        expected = {"value": "condition", "type": "TEST_NOT"}
        self.assertEqual(result, expected, "Not matched.")

    def test_test_case8(self):

        text = "!condition(some, value)"
        tree = get_parser("test").parse(text)
        print(tree)
        result = CommonTransformer().transform(tree)
        print(result)
        expected = {
            "value": {
                "name": "condition",
                "type": "INVOCATION",
                "args": ["some", "value"],
            },
            "type": "TEST_NOT",
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_test_case9(self):

        text = '"String".equals(Object)'
        tree = get_parser("test").parse(text)
        print(tree)
        result = CommonTransformer().transform(tree)
        print(result)
        expected = {"name": '"String".equals', "type": "INVOCATION", "args": ["Object"]}
        self.assertEqual(result, expected, "Not matched.")

    def test_test_case10(self):

        text = 'left.method("Arg") <= rightPart(this, that)'
        tree = get_parser("test").parse(text)
        print(tree)
        result = CommonTransformer().transform(tree)
        print(result)
        expected = {
            "left": {"name": "left.method", "type": "INVOCATION", "args": ['"Arg"']},
            "chain": [
                {
                    "value": {
                        "name": "rightPart",
                        "type": "INVOCATION",
                        "args": ["this", "that"],
                    },
                    "operator": "<=",
                }
            ],
            "type": "COMPARISON",
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_test_case11(self):

        text = "i <= 10"
        tree = get_parser("test").parse(text)
        print(tree)
        result = CommonTransformer().transform(tree)
        print(result)
        expected = {
            "left": "i",
            "chain": [{"value": 10, "operator": "<="}],
            "type": "COMPARISON",
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_test_case12(self):

        text = """
        (part1 || part2 && (another && !more || last)) || part3 && part4 || part5
        """

        tree = get_parser("test").parse(text)
        print(tree)
        result = CommonTransformer().transform(tree)
        print(result)
        expected = {
            "left": {
                "left": "part1",
                "right": [
                    {
                        "left": "part2",
                        "right": [
                            {
                                "left": {
                                    "left": "another",
                                    "right": [{"value": "more", "type": "TEST_NOT"}],
                                    "type": "TEST_AND",
                                },
                                "right": ["last"],
                                "type": "TEST_OR",
                            }
                        ],
                        "type": "TEST_AND",
                    }
                ],
                "type": "TEST_OR",
            },
            "right": [
                {"left": "part3", "right": ["part4"], "type": "TEST_AND"},
                "part5",
            ],
            "type": "TEST_OR",
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_test_case13(self):

        text = "++i"
        tree = get_parser("test").parse(text)
        print(tree)
        result = CommonTransformer().transform(tree)
        print(result)
        expected = {"value": "i", "operator": "++", "type": "BINARY_BEFORE_EXPRESSION"}
        self.assertEqual(result, expected, "Not matched.")

    def test_test_case14(self):

        text = "i--"
        tree = get_parser("test").parse(text)
        print(tree)
        result = CommonTransformer().transform(tree)
        print(result)
        expected = {"value": "i", "operator": "--", "type": "BINARY_AFTER_EXPRESSION"}
        self.assertEqual(result, expected, "Not matched.")
