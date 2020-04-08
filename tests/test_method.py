import unittest
from tests.helper import get_parser
from java_parser.method import MethodTransformer
from java_parser.common import CommonTransformer


class TestMethodTransformer(CommonTransformer, MethodTransformer):
    pass


class TestMethod(unittest.TestCase):
    def test_stmt_case1(self):

        text = "break;"
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {"name": "break", "type": "BREAK", "lineno": 1, "linenoEnd": 1}
        self.assertEqual(result, expected, "Not matched.")

    def test_stmt_case2(self):

        text = "continue;"
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {"name": "continue", "type": "CONTINUE", "lineno": 1, "linenoEnd": 1}
        self.assertEqual(result, expected, "Not matched.")

    def test_stmt_case3(self):

        text = "return;"
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {"name": "return", "type": "RETURN", "lineno": 1, "linenoEnd": 1}
        self.assertEqual(result, expected, "Not matched.")

    def test_stmt_case4(self):

        text = "return something(args);"
        tree = get_parser("stmt").parse(text)
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
        tree = get_parser("stmt").parse(text)
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

    def test_stmt_case6(self):

        text = 'private static String name = "Real Name";'
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {
            "name": "name",
            "assign": '"Real Name"',
            "classType": "String",
            "modifiers": ["private", "static"],
            "type": "STATEMENT",
            "lineno": 1,
            "linenoEnd": 1,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_stmt_case7(self):

        text = "int thisNumber = self++;"
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {
            "classType": "int",
            "name": "thisNumber",
            "assign": {
                "value": "self",
                "operator": "++",
                "type": "BINARY_AFTER_EXPRESSION",
            },
            "type": "STATEMENT",
            "lineno": 1,
            "linenoEnd": 1,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_stmt_case8(self):

        text = "String name = (String) SomeVariable.attribute;"
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {
            "classType": "String",
            "name": "name",
            "assign": {
                "value": "SomeVariable.attribute",
                "cast": "String",
                "type": "CAST_EXPRESSION",
            },
            "type": "STATEMENT",
            "lineno": 1,
            "linenoEnd": 1,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_stmt_case9(self):

        text = "String name = (ArrayList<String>)SomeVariable.attribute;"
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {
            "classType": "String",
            "name": "name",
            "assign": {
                "value": "SomeVariable.attribute",
                "cast": {"name": "ArrayList", "generic": "String"},
                "type": "CAST_EXPRESSION",
            },
            "type": "STATEMENT",
            "lineno": 1,
            "linenoEnd": 1,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_stmt_case10(self):

        text = "return sb2.toString() + WHERE_START + sb.toString() + WHERE_END;"
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {
            "name": "return",
            "type": "RETURN",
            "lineno": 1,
            "linenoEnd": 1,
            "value": {
                "left": {"name": "sb2.toString", "type": "INVOCATION"},
                "chain": [
                    {"value": "WHERE_START", "operator": "+"},
                    {
                        "value": {"name": "sb.toString", "type": "INVOCATION"},
                        "operator": "+",
                    },
                    {"value": "WHERE_END", "operator": "+"},
                ],
                "type": "ARITHMETIC_EXPRESSION",
            },
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_stmt_case11(self):

        text = 'assertThat(response.getBody().equals("Greetings from Spring Boot!"));'
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {
            "name": {
                "name": "assertThat",
                "type": "INVOCATION",
                "args": [
                    {
                        "name": {
                            "base": {"name": "response.getBody", "type": "INVOCATION"},
                            "name": "equals",
                            "type": "ATTRIBUTE",
                        },
                        "type": "INVOCATION",
                        "args": ['"Greetings from Spring Boot!"'],
                    }
                ],
            },
            "type": "STATEMENT",
            "lineno": 1,
            "linenoEnd": 1,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_stmt_case12(self):

        text = "doSomeThingHere(Parameter);"
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {
            "name": {
                "name": "doSomeThingHere",
                "type": "INVOCATION",
                "args": ["Parameter"],
            },
            "type": "STATEMENT",
            "lineno": 1,
            "linenoEnd": 1,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_suit_case1(self):

        text = """
        doSomeThingHere(Parameter);
        doSomeThingHere(Parameter);
        doSomeThingHere(Parameter);
        doSomeThingHere(Parameter);
        """
        tree = get_parser("suit").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = [
            {
                "name": {
                    "name": "doSomeThingHere",
                    "type": "INVOCATION",
                    "args": ["Parameter"],
                },
                "type": "STATEMENT",
                "lineno": 2,
                "linenoEnd": 2,
            },
            {
                "name": {
                    "name": "doSomeThingHere",
                    "type": "INVOCATION",
                    "args": ["Parameter"],
                },
                "type": "STATEMENT",
                "lineno": 3,
                "linenoEnd": 3,
            },
            {
                "name": {
                    "name": "doSomeThingHere",
                    "type": "INVOCATION",
                    "args": ["Parameter"],
                },
                "type": "STATEMENT",
                "lineno": 4,
                "linenoEnd": 4,
            },
            {
                "name": {
                    "name": "doSomeThingHere",
                    "type": "INVOCATION",
                    "args": ["Parameter"],
                },
                "type": "STATEMENT",
                "lineno": 5,
                "linenoEnd": 5,
            },
        ]
        self.assertEqual(result, expected, "Not matched.")

    def test_suit_case2(self):

        text = """
        if (someConditions) {
            doSomeThingHere(Parameter);
            doSomeThingHere(Parameter);
            doSomeThingHere(Parameter);
        } else {
            maybeSomeCleanUpHere();
        }
        if (another) {
            doSomeThingHere(Parameter);
        } else {
            maybeSomeCleanUpHere();
        }"""
        tree = get_parser("suit").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = [
            {
                "type": "IF",
                "test": "someConditions",
                "lineno": 2,
                "linenoEnd": 8,
                "value": [
                    {
                        "name": {
                            "name": "doSomeThingHere",
                            "type": "INVOCATION",
                            "args": ["Parameter"],
                        },
                        "type": "STATEMENT",
                        "lineno": 3,
                        "linenoEnd": 3,
                    },
                    {
                        "name": {
                            "name": "doSomeThingHere",
                            "type": "INVOCATION",
                            "args": ["Parameter"],
                        },
                        "type": "STATEMENT",
                        "lineno": 4,
                        "linenoEnd": 4,
                    },
                    {
                        "name": {
                            "name": "doSomeThingHere",
                            "type": "INVOCATION",
                            "args": ["Parameter"],
                        },
                        "type": "STATEMENT",
                        "lineno": 5,
                        "linenoEnd": 5,
                    },
                ],
                "chain": [
                    {
                        "type": "ELSE",
                        "lineno": 6,
                        "linenoEnd": 8,
                        "value": [
                            {
                                "name": {
                                    "name": "maybeSomeCleanUpHere",
                                    "type": "INVOCATION",
                                },
                                "type": "STATEMENT",
                                "lineno": 7,
                                "linenoEnd": 7,
                            }
                        ],
                    }
                ],
            },
            {
                "type": "IF",
                "test": "another",
                "lineno": 9,
                "linenoEnd": 13,
                "value": [
                    {
                        "name": {
                            "name": "doSomeThingHere",
                            "type": "INVOCATION",
                            "args": ["Parameter"],
                        },
                        "type": "STATEMENT",
                        "lineno": 10,
                        "linenoEnd": 10,
                    }
                ],
                "chain": [
                    {
                        "type": "ELSE",
                        "lineno": 11,
                        "linenoEnd": 13,
                        "value": [
                            {
                                "name": {
                                    "name": "maybeSomeCleanUpHere",
                                    "type": "INVOCATION",
                                },
                                "type": "STATEMENT",
                                "lineno": 12,
                                "linenoEnd": 12,
                            }
                        ],
                    }
                ],
            },
        ]
        self.assertEqual(result, expected, "Not matched.")

    def test_suit_case3(self):

        text = """
        if (someConditions) {
            doSomeThingHere1(Parameter);
            doSomeThingHere2(Parameter);
            doSomeThingHere3(Parameter);
        }
        if (another) {
            doSomeThingHere(Parameter);
        }"""
        tree = get_parser("suit").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = [
            {
                "type": "IF",
                "test": "someConditions",
                "lineno": 2,
                "linenoEnd": 6,
                "value": [
                    {
                        "name": {
                            "name": "doSomeThingHere1",
                            "type": "INVOCATION",
                            "args": ["Parameter"],
                        },
                        "type": "STATEMENT",
                        "lineno": 3,
                        "linenoEnd": 3,
                    },
                    {
                        "name": {
                            "name": "doSomeThingHere2",
                            "type": "INVOCATION",
                            "args": ["Parameter"],
                        },
                        "type": "STATEMENT",
                        "lineno": 4,
                        "linenoEnd": 4,
                    },
                    {
                        "name": {
                            "name": "doSomeThingHere3",
                            "type": "INVOCATION",
                            "args": ["Parameter"],
                        },
                        "type": "STATEMENT",
                        "lineno": 5,
                        "linenoEnd": 5,
                    },
                ],
            },
            {
                "type": "IF",
                "test": "another",
                "lineno": 7,
                "linenoEnd": 9,
                "value": [
                    {
                        "name": {
                            "name": "doSomeThingHere",
                            "type": "INVOCATION",
                            "args": ["Parameter"],
                        },
                        "type": "STATEMENT",
                        "lineno": 8,
                        "linenoEnd": 8,
                    }
                ],
            },
        ]
        self.assertEqual(result, expected, "Not matched.")

    def test_if_case1(self):

        text = """
        if (someConditions) {
            doSomeThingHere(Parameter);
        }"""
        tree = get_parser("if_stmt").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {
            "type": "IF",
            "test": "someConditions",
            "lineno": 2,
            "linenoEnd": 4,
            "value": [
                {
                    "name": {
                        "name": "doSomeThingHere",
                        "type": "INVOCATION",
                        "args": ["Parameter"],
                    },
                    "type": "STATEMENT",
                    "lineno": 3,
                    "linenoEnd": 3,
                }
            ],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_if_case2(self):

        text = """
        if (someConditions) {
            doSomeThingHere(Parameter);
            doSomeThingHere(Parameter);
            doSomeThingHere(Parameter);
        } else {
            maybeSomeCleanUpHere();
        }"""
        tree = get_parser("if_stmt").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {
            "type": "IF",
            "test": "someConditions",
            "lineno": 2,
            "linenoEnd": 8,
            "value": [
                {
                    "name": {
                        "name": "doSomeThingHere",
                        "type": "INVOCATION",
                        "args": ["Parameter"],
                    },
                    "type": "STATEMENT",
                    "lineno": 3,
                    "linenoEnd": 3,
                },
                {
                    "name": {
                        "name": "doSomeThingHere",
                        "type": "INVOCATION",
                        "args": ["Parameter"],
                    },
                    "type": "STATEMENT",
                    "lineno": 4,
                    "linenoEnd": 4,
                },
                {
                    "name": {
                        "name": "doSomeThingHere",
                        "type": "INVOCATION",
                        "args": ["Parameter"],
                    },
                    "type": "STATEMENT",
                    "lineno": 5,
                    "linenoEnd": 5,
                },
            ],
            "chain": [
                {
                    "type": "ELSE",
                    "lineno": 6,
                    "linenoEnd": 8,
                    "value": [
                        {
                            "name": {
                                "name": "maybeSomeCleanUpHere",
                                "type": "INVOCATION",
                            },
                            "type": "STATEMENT",
                            "lineno": 7,
                            "linenoEnd": 7,
                        }
                    ],
                }
            ],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_if_case3(self):

        text = """
        if (someConditions) {
            doSomeThingHere(Parameter);
            doSomeThingHere(Parameter);
            doSomeThingHere(Parameter);
        } else if (otherConditions) {
            doOtherThingHere(OtherParameter);
            doOtherThingHere(OtherParameter);
            doOtherThingHere(OtherParameter);
        } else {
            maybeSomeCleanUpHere();
        }"""
        tree = get_parser("if_stmt").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {
            "type": "IF",
            "test": "someConditions",
            "lineno": 2,
            "linenoEnd": 12,
            "value": [
                {
                    "name": {
                        "name": "doSomeThingHere",
                        "type": "INVOCATION",
                        "args": ["Parameter"],
                    },
                    "type": "STATEMENT",
                    "lineno": 3,
                    "linenoEnd": 3,
                },
                {
                    "name": {
                        "name": "doSomeThingHere",
                        "type": "INVOCATION",
                        "args": ["Parameter"],
                    },
                    "type": "STATEMENT",
                    "lineno": 4,
                    "linenoEnd": 4,
                },
                {
                    "name": {
                        "name": "doSomeThingHere",
                        "type": "INVOCATION",
                        "args": ["Parameter"],
                    },
                    "type": "STATEMENT",
                    "lineno": 5,
                    "linenoEnd": 5,
                },
            ],
            "chain": [
                {
                    "type": "ELSE_IF",
                    "test": "otherConditions",
                    "lineno": 6,
                    "linenoEnd": 10,
                    "value": [
                        {
                            "name": {
                                "name": "doOtherThingHere",
                                "type": "INVOCATION",
                                "args": ["OtherParameter"],
                            },
                            "type": "STATEMENT",
                            "lineno": 7,
                            "linenoEnd": 7,
                        },
                        {
                            "name": {
                                "name": "doOtherThingHere",
                                "type": "INVOCATION",
                                "args": ["OtherParameter"],
                            },
                            "type": "STATEMENT",
                            "lineno": 8,
                            "linenoEnd": 8,
                        },
                        {
                            "name": {
                                "name": "doOtherThingHere",
                                "type": "INVOCATION",
                                "args": ["OtherParameter"],
                            },
                            "type": "STATEMENT",
                            "lineno": 9,
                            "linenoEnd": 9,
                        },
                    ],
                },
                {
                    "type": "ELSE",
                    "lineno": 10,
                    "linenoEnd": 12,
                    "value": [
                        {
                            "name": {
                                "name": "maybeSomeCleanUpHere",
                                "type": "INVOCATION",
                            },
                            "type": "STATEMENT",
                            "lineno": 11,
                            "linenoEnd": 11,
                        }
                    ],
                },
            ],
        }
        a = {
            "type": "IF",
            "test": "someConditions",
            "lineno": 2,
            "linenoEnd": 12,
            "value": [
                {
                    "name": {
                        "name": "doSomeThingHere",
                        "type": "INVOCATION",
                        "args": ["Parameter"],
                    },
                    "type": "STATEMENT",
                    "lineno": 3,
                    "linenoEnd": 3,
                },
                {
                    "name": {
                        "name": "doSomeThingHere",
                        "type": "INVOCATION",
                        "args": ["Parameter"],
                    },
                    "type": "STATEMENT",
                    "lineno": 4,
                    "linenoEnd": 4,
                },
                {
                    "name": {
                        "name": "doSomeThingHere",
                        "type": "INVOCATION",
                        "args": ["Parameter"],
                    },
                    "type": "STATEMENT",
                    "lineno": 5,
                    "linenoEnd": 5,
                },
            ],
            "chain": [
                {
                    "type": "ELSE",
                    "lineno": 6,
                    "linenoEnd": 12,
                    "value": [
                        {
                            "type": "IF",
                            "test": "otherConditions",
                            "lineno": 6,
                            "linenoEnd": 12,
                            "value": [
                                {
                                    "name": {
                                        "name": "doOtherThingHere",
                                        "type": "INVOCATION",
                                        "args": ["OtherParameter"],
                                    },
                                    "type": "STATEMENT",
                                    "lineno": 7,
                                    "linenoEnd": 7,
                                },
                                {
                                    "name": {
                                        "name": "doOtherThingHere",
                                        "type": "INVOCATION",
                                        "args": ["OtherParameter"],
                                    },
                                    "type": "STATEMENT",
                                    "lineno": 8,
                                    "linenoEnd": 8,
                                },
                                {
                                    "name": {
                                        "name": "doOtherThingHere",
                                        "type": "INVOCATION",
                                        "args": ["OtherParameter"],
                                    },
                                    "type": "STATEMENT",
                                    "lineno": 9,
                                    "linenoEnd": 9,
                                },
                            ],
                            "chain": [
                                {
                                    "type": "ELSE",
                                    "lineno": 10,
                                    "linenoEnd": 12,
                                    "value": [
                                        {
                                            "name": {
                                                "name": "maybeSomeCleanUpHere",
                                                "type": "INVOCATION",
                                            },
                                            "type": "STATEMENT",
                                            "lineno": 11,
                                            "linenoEnd": 11,
                                        }
                                    ],
                                }
                            ],
                        }
                    ],
                }
            ],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_if_case4(self):

        text = """
        if (someConditions) {
            if (another) {
                doSomeThingHere(Parameter);
            } else {
                maybeSomeCleanUpHere();
            }
            doSomeThingHere(Parameter);
            doSomeThingHere(Parameter);
            doSomeThingHere(Parameter);
        } else {
            maybeSomeCleanUpHere();
        }"""
        tree = get_parser("if_stmt").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {
            "type": "IF",
            "test": "someConditions",
            "lineno": 2,
            "linenoEnd": 13,
            "value": [
                {
                    "type": "IF",
                    "test": "another",
                    "lineno": 3,
                    "linenoEnd": 7,
                    "value": [
                        {
                            "name": {
                                "name": "doSomeThingHere",
                                "type": "INVOCATION",
                                "args": ["Parameter"],
                            },
                            "type": "STATEMENT",
                            "lineno": 4,
                            "linenoEnd": 4,
                        }
                    ],
                    "chain": [
                        {
                            "type": "ELSE",
                            "lineno": 5,
                            "linenoEnd": 7,
                            "value": [
                                {
                                    "name": {
                                        "name": "maybeSomeCleanUpHere",
                                        "type": "INVOCATION",
                                    },
                                    "type": "STATEMENT",
                                    "lineno": 6,
                                    "linenoEnd": 6,
                                }
                            ],
                        }
                    ],
                },
                {
                    "name": {
                        "name": "doSomeThingHere",
                        "type": "INVOCATION",
                        "args": ["Parameter"],
                    },
                    "type": "STATEMENT",
                    "lineno": 8,
                    "linenoEnd": 8,
                },
                {
                    "name": {
                        "name": "doSomeThingHere",
                        "type": "INVOCATION",
                        "args": ["Parameter"],
                    },
                    "type": "STATEMENT",
                    "lineno": 9,
                    "linenoEnd": 9,
                },
                {
                    "name": {
                        "name": "doSomeThingHere",
                        "type": "INVOCATION",
                        "args": ["Parameter"],
                    },
                    "type": "STATEMENT",
                    "lineno": 10,
                    "linenoEnd": 10,
                },
            ],
            "chain": [
                {
                    "type": "ELSE",
                    "lineno": 11,
                    "linenoEnd": 13,
                    "value": [
                        {
                            "name": {
                                "name": "maybeSomeCleanUpHere",
                                "type": "INVOCATION",
                            },
                            "type": "STATEMENT",
                            "lineno": 12,
                            "linenoEnd": 12,
                        }
                    ],
                }
            ],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_if_case5(self):

        text = """
        if (someConditions)
            doSomeThingHere1(Parameter);
        else if (another)
            doSomeThingHere2(Parameter);
        else
            doSomeThingHere3(Parameter);"""
        tree = get_parser("if_stmt").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {
            "type": "IF",
            "test": "someConditions",
            "lineno": 2,
            "linenoEnd": 7,
            "value": [
                {
                    "name": {
                        "name": "doSomeThingHere1",
                        "type": "INVOCATION",
                        "args": ["Parameter"],
                    },
                    "type": "STATEMENT",
                    "lineno": 3,
                    "linenoEnd": 3,
                }
            ],
            "chain": [
                {
                    "type": "ELSE_IF",
                    "test": "another",
                    "lineno": 4,
                    "linenoEnd": 5,
                    "value": [
                        {
                            "name": {
                                "name": "doSomeThingHere2",
                                "type": "INVOCATION",
                                "args": ["Parameter"],
                            },
                            "type": "STATEMENT",
                            "lineno": 5,
                            "linenoEnd": 5,
                        }
                    ],
                },
                {
                    "type": "ELSE",
                    "lineno": 6,
                    "linenoEnd": 7,
                    "value": [
                        {
                            "name": {
                                "name": "doSomeThingHere3",
                                "type": "INVOCATION",
                                "args": ["Parameter"],
                            },
                            "type": "STATEMENT",
                            "lineno": 7,
                            "linenoEnd": 7,
                        }
                    ],
                },
            ],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_switch_case1(self):

        text = """
        switch(mode) {
        }"""
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {"test": "mode", "type": "SWITCH", "lineno": 2, "linenoEnd": 3}
        self.assertEqual(result, expected, "Not matched.")

    def test_switch_case2(self):

        text = """
            switch(mode){
                case "MODE_1":
                    break;
            }"""
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {
            "test": "mode",
            "type": "SWITCH",
            "lineno": 2,
            "linenoEnd": 5,
            "cases": [
                {
                    "caseKey": ['"MODE_1"'],
                    "value": [
                        {"name": "break", "type": "BREAK", "lineno": 4, "linenoEnd": 4}
                    ],
                    "type": "CASE",
                    "lineno": 3,
                    "linenoEnd": 4,
                }
            ],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_switch_case3(self):

        text = """
            switch(mode){
                case "MODE_1":
                    doSomething();
                    doSomething();
                    doSomething();
                    break;
            }"""
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {
            "test": "mode",
            "type": "SWITCH",
            "lineno": 2,
            "linenoEnd": 8,
            "cases": [
                {
                    "caseKey": ['"MODE_1"'],
                    "value": [
                        {
                            "name": {"name": "doSomething", "type": "INVOCATION"},
                            "type": "STATEMENT",
                            "lineno": 4,
                            "linenoEnd": 4,
                        },
                        {
                            "name": {"name": "doSomething", "type": "INVOCATION"},
                            "type": "STATEMENT",
                            "lineno": 5,
                            "linenoEnd": 5,
                        },
                        {
                            "name": {"name": "doSomething", "type": "INVOCATION"},
                            "type": "STATEMENT",
                            "lineno": 6,
                            "linenoEnd": 6,
                        },
                        {"name": "break", "type": "BREAK", "lineno": 7, "linenoEnd": 7},
                    ],
                    "type": "CASE",
                    "lineno": 3,
                    "linenoEnd": 7,
                }
            ],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_switch_case4(self):

        text = """
            switch(mode){
                case "MODE_1":
                    doSomething();
                    doSomething();
                    break;
                case "MODE_2":
                    doSomething();
                    break;
            }"""
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {
            "test": "mode",
            "type": "SWITCH",
            "lineno": 2,
            "linenoEnd": 10,
            "cases": [
                {
                    "caseKey": ['"MODE_1"'],
                    "value": [
                        {
                            "name": {"name": "doSomething", "type": "INVOCATION"},
                            "type": "STATEMENT",
                            "lineno": 4,
                            "linenoEnd": 4,
                        },
                        {
                            "name": {"name": "doSomething", "type": "INVOCATION"},
                            "type": "STATEMENT",
                            "lineno": 5,
                            "linenoEnd": 5,
                        },
                        {"name": "break", "type": "BREAK", "lineno": 6, "linenoEnd": 6},
                    ],
                    "type": "CASE",
                    "lineno": 3,
                    "linenoEnd": 6,
                },
                {
                    "caseKey": ['"MODE_2"'],
                    "value": [
                        {
                            "name": {"name": "doSomething", "type": "INVOCATION"},
                            "type": "STATEMENT",
                            "lineno": 8,
                            "linenoEnd": 8,
                        },
                        {"name": "break", "type": "BREAK", "lineno": 9, "linenoEnd": 9},
                    ],
                    "type": "CASE",
                    "lineno": 7,
                    "linenoEnd": 9,
                },
            ],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_switch_case5(self):

        text = """
            switch(mode){
                default:
                    doNothing();
                    break;
            }"""
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {
            "test": "mode",
            "type": "SWITCH",
            "lineno": 2,
            "linenoEnd": 6,
            "cases": [
                {
                    "caseKey": ["<default>"],
                    "value": [
                        {
                            "name": {"name": "doNothing", "type": "INVOCATION"},
                            "type": "STATEMENT",
                            "lineno": 4,
                            "linenoEnd": 4,
                        },
                        {"name": "break", "type": "BREAK", "lineno": 5, "linenoEnd": 5},
                    ],
                    "type": "CASE",
                    "lineno": 3,
                    "linenoEnd": 5,
                }
            ],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_switch_case6(self):

        text = """switch(mode){
                default:
                    doNothing();
                    doNothing();
                    doNothing();
                    break;
            }"""
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {
            "test": "mode",
            "type": "SWITCH",
            "lineno": 1,
            "linenoEnd": 7,
            "cases": [
                {
                    "caseKey": ["<default>"],
                    "value": [
                        {
                            "name": {"name": "doNothing", "type": "INVOCATION"},
                            "type": "STATEMENT",
                            "lineno": 3,
                            "linenoEnd": 3,
                        },
                        {
                            "name": {"name": "doNothing", "type": "INVOCATION"},
                            "type": "STATEMENT",
                            "lineno": 4,
                            "linenoEnd": 4,
                        },
                        {
                            "name": {"name": "doNothing", "type": "INVOCATION"},
                            "type": "STATEMENT",
                            "lineno": 5,
                            "linenoEnd": 5,
                        },
                        {"name": "break", "type": "BREAK", "lineno": 6, "linenoEnd": 6},
                    ],
                    "type": "CASE",
                    "lineno": 2,
                    "linenoEnd": 6,
                }
            ],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_switch_case7(self):

        text = """switch(mode){
                case ABC:
                default:
                    doNothing();
                    doNothing();
                    doNothing();
                    break;
            }"""
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {
            "test": "mode",
            "type": "SWITCH",
            "lineno": 1,
            "linenoEnd": 8,
            "cases": [
                {
                    "caseKey": ["ABC", "<default>"],
                    "value": [
                        {
                            "name": {"name": "doNothing", "type": "INVOCATION"},
                            "type": "STATEMENT",
                            "lineno": 4,
                            "linenoEnd": 4,
                        },
                        {
                            "name": {"name": "doNothing", "type": "INVOCATION"},
                            "type": "STATEMENT",
                            "lineno": 5,
                            "linenoEnd": 5,
                        },
                        {
                            "name": {"name": "doNothing", "type": "INVOCATION"},
                            "type": "STATEMENT",
                            "lineno": 6,
                            "linenoEnd": 6,
                        },
                        {"name": "break", "type": "BREAK", "lineno": 7, "linenoEnd": 7},
                    ],
                    "type": "CASE",
                    "lineno": 2,
                    "linenoEnd": 7,
                }
            ],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_switch_case7(self):

        text = """switch(mode){
                case ABC:
                    doNothing();
                    break;
                default:
                    doNothing();
                    doNothing();
                    doNothing();
                    break;
            }"""
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {
            "test": "mode",
            "type": "SWITCH",
            "lineno": 1,
            "linenoEnd": 8,
            "cases": [
                {
                    "caseKey": ["ABC", "<default>"],
                    "value": [
                        {
                            "name": {"name": "doNothing", "type": "INVOCATION"},
                            "type": "STATEMENT",
                            "lineno": 4,
                            "linenoEnd": 4,
                        },
                        {
                            "name": {"name": "doNothing", "type": "INVOCATION"},
                            "type": "STATEMENT",
                            "lineno": 5,
                            "linenoEnd": 5,
                        },
                        {
                            "name": {"name": "doNothing", "type": "INVOCATION"},
                            "type": "STATEMENT",
                            "lineno": 6,
                            "linenoEnd": 6,
                        },
                        {"name": "break", "type": "BREAK", "lineno": 7, "linenoEnd": 7},
                    ],
                    "type": "CASE",
                    "lineno": 2,
                    "linenoEnd": 7,
                }
            ],
        }
        self.assertEqual(result, expected, "Not matched.")
