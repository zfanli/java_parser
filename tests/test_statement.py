import unittest
from tests.helper import get_parser
from java_parser.enum import EnumTransformer
from java_parser.method import MethodTransformer
from java_parser.common import CommonTransformer


class TestMethodTransformer(CommonTransformer, MethodTransformer, EnumTransformer):
    pass


class TestStatement(unittest.TestCase):
    def test_stmt_case1(self):

        text = "break;"
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {"body": "break", "type": "BREAK", "lineno": 1, "linenoEnd": 1}
        self.assertEqual(result, expected, "Not matched.")

    def test_stmt_case2(self):

        text = "continue;"
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {"body": "continue", "type": "CONTINUE", "lineno": 1, "linenoEnd": 1}
        self.assertEqual(result, expected, "Not matched.")

    def test_stmt_case3(self):

        text = "return;"
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {"body": "return", "type": "RETURN", "lineno": 1, "linenoEnd": 1}
        self.assertEqual(result, expected, "Not matched.")

    def test_stmt_case4(self):

        text = "return something(args);"
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {
            "type": "RETURN",
            "body": {"name": "something", "type": "INVOCATION", "args": ["args"]},
            "lineno": 1,
            "linenoEnd": 1,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_stmt_case5(self):

        text = 'throw new Exception("Something went wrong");'
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {
            "type": "THROW",
            "body": {
                "value": {
                    "name": "Exception",
                    "type": "INVOCATION",
                    "args": ['"Something went wrong"'],
                },
                "type": "NEW_EXPRESSION",
            },
            "lineno": 1,
            "linenoEnd": 1,
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
            "name": "name",
            "assign": {
                "value": "SomeVariable.attribute",
                "cast": {"name": "ArrayList", "generic": ["String"]},
                "type": "CAST_EXPRESSION",
            },
            "classType": "String",
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
            "body": {
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
            "type": "RETURN",
            "lineno": 1,
            "linenoEnd": 1,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_stmt_case11(self):

        text = 'assertThat(response.getBody().equals("Greetings from Spring Boot!"));'
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {
            "body": {
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
            "body": {
                "name": "doSomeThingHere",
                "type": "INVOCATION",
                "args": ["Parameter"],
            },
            "type": "STATEMENT",
            "lineno": 1,
            "linenoEnd": 1,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_stmt_case13(self):

        text = "(SomeType)doSomeThingHere(Parameter).doSomething();"
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {
            "body": {
                "value": {
                    "name": {
                        "base": {
                            "name": "doSomeThingHere",
                            "type": "INVOCATION",
                            "args": ["Parameter"],
                        },
                        "name": "doSomething",
                        "type": "ATTRIBUTE",
                    },
                    "type": "INVOCATION",
                },
                "cast": "SomeType",
                "type": "CAST_EXPRESSION",
            },
            "type": "STATEMENT",
            "lineno": 1,
            "linenoEnd": 1,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_stmt_case14(self):

        text = "object = factory.makeObject(param);"
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {
            "name": "object",
            "assign": {
                "name": "factory.makeObject",
                "type": "INVOCATION",
                "args": ["param"],
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
                "body": {
                    "name": "doSomeThingHere",
                    "type": "INVOCATION",
                    "args": ["Parameter"],
                },
                "type": "STATEMENT",
                "lineno": 2,
                "linenoEnd": 2,
            },
            {
                "body": {
                    "name": "doSomeThingHere",
                    "type": "INVOCATION",
                    "args": ["Parameter"],
                },
                "type": "STATEMENT",
                "lineno": 3,
                "linenoEnd": 3,
            },
            {
                "body": {
                    "name": "doSomeThingHere",
                    "type": "INVOCATION",
                    "args": ["Parameter"],
                },
                "type": "STATEMENT",
                "lineno": 4,
                "linenoEnd": 4,
            },
            {
                "body": {
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
                "body": [
                    {
                        "body": {
                            "name": "doSomeThingHere",
                            "type": "INVOCATION",
                            "args": ["Parameter"],
                        },
                        "type": "STATEMENT",
                        "lineno": 3,
                        "linenoEnd": 3,
                    },
                    {
                        "body": {
                            "name": "doSomeThingHere",
                            "type": "INVOCATION",
                            "args": ["Parameter"],
                        },
                        "type": "STATEMENT",
                        "lineno": 4,
                        "linenoEnd": 4,
                    },
                    {
                        "body": {
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
                        "body": [
                            {
                                "body": {
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
                "body": [
                    {
                        "body": {
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
                        "body": [
                            {
                                "body": {
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
                "body": [
                    {
                        "body": {
                            "name": "doSomeThingHere1",
                            "type": "INVOCATION",
                            "args": ["Parameter"],
                        },
                        "type": "STATEMENT",
                        "lineno": 3,
                        "linenoEnd": 3,
                    },
                    {
                        "body": {
                            "name": "doSomeThingHere2",
                            "type": "INVOCATION",
                            "args": ["Parameter"],
                        },
                        "type": "STATEMENT",
                        "lineno": 4,
                        "linenoEnd": 4,
                    },
                    {
                        "body": {
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
                "body": [
                    {
                        "body": {
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
            "body": [
                {
                    "body": {
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
            "body": [
                {
                    "body": {
                        "name": "doSomeThingHere",
                        "type": "INVOCATION",
                        "args": ["Parameter"],
                    },
                    "type": "STATEMENT",
                    "lineno": 3,
                    "linenoEnd": 3,
                },
                {
                    "body": {
                        "name": "doSomeThingHere",
                        "type": "INVOCATION",
                        "args": ["Parameter"],
                    },
                    "type": "STATEMENT",
                    "lineno": 4,
                    "linenoEnd": 4,
                },
                {
                    "body": {
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
                    "body": [
                        {
                            "body": {
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
            "body": [
                {
                    "body": {
                        "name": "doSomeThingHere",
                        "type": "INVOCATION",
                        "args": ["Parameter"],
                    },
                    "type": "STATEMENT",
                    "lineno": 3,
                    "linenoEnd": 3,
                },
                {
                    "body": {
                        "name": "doSomeThingHere",
                        "type": "INVOCATION",
                        "args": ["Parameter"],
                    },
                    "type": "STATEMENT",
                    "lineno": 4,
                    "linenoEnd": 4,
                },
                {
                    "body": {
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
                    "body": [
                        {
                            "body": {
                                "name": "doOtherThingHere",
                                "type": "INVOCATION",
                                "args": ["OtherParameter"],
                            },
                            "type": "STATEMENT",
                            "lineno": 7,
                            "linenoEnd": 7,
                        },
                        {
                            "body": {
                                "name": "doOtherThingHere",
                                "type": "INVOCATION",
                                "args": ["OtherParameter"],
                            },
                            "type": "STATEMENT",
                            "lineno": 8,
                            "linenoEnd": 8,
                        },
                        {
                            "body": {
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
                    "body": [
                        {
                            "body": {
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
            "body": [
                {
                    "type": "IF",
                    "test": "another",
                    "lineno": 3,
                    "linenoEnd": 7,
                    "body": [
                        {
                            "body": {
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
                            "body": [
                                {
                                    "body": {
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
                    "body": {
                        "name": "doSomeThingHere",
                        "type": "INVOCATION",
                        "args": ["Parameter"],
                    },
                    "type": "STATEMENT",
                    "lineno": 8,
                    "linenoEnd": 8,
                },
                {
                    "body": {
                        "name": "doSomeThingHere",
                        "type": "INVOCATION",
                        "args": ["Parameter"],
                    },
                    "type": "STATEMENT",
                    "lineno": 9,
                    "linenoEnd": 9,
                },
                {
                    "body": {
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
                    "body": [
                        {
                            "body": {
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
            "body": [
                {
                    "body": {
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
                    "body": [
                        {
                            "body": {
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
                    "body": [
                        {
                            "body": {
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

    def test_if_case6(self):

        text = """
        if (!object.equals(another.CONSTANT_VARIABLE)) {
            something();
        }"""
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {
            "type": "IF",
            "test": {
                "value": {
                    "name": "object.equals",
                    "type": "INVOCATION",
                    "args": ["another.CONSTANT_VARIABLE"],
                },
                "type": "TEST_NOT",
            },
            "lineno": 2,
            "linenoEnd": 4,
            "body": [
                {
                    "body": {"name": "something", "type": "INVOCATION"},
                    "type": "STATEMENT",
                    "lineno": 3,
                    "linenoEnd": 3,
                }
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
                    "caseKey": '"MODE_1"',
                    "type": "CASE",
                    "lineno": 3,
                    "linenoEnd": 4,
                    "body": [
                        {"body": "break", "type": "BREAK", "lineno": 4, "linenoEnd": 4}
                    ],
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
                    "caseKey": '"MODE_1"',
                    "type": "CASE",
                    "lineno": 3,
                    "linenoEnd": 7,
                    "body": [
                        {
                            "body": {"name": "doSomething", "type": "INVOCATION"},
                            "type": "STATEMENT",
                            "lineno": 4,
                            "linenoEnd": 4,
                        },
                        {
                            "body": {"name": "doSomething", "type": "INVOCATION"},
                            "type": "STATEMENT",
                            "lineno": 5,
                            "linenoEnd": 5,
                        },
                        {
                            "body": {"name": "doSomething", "type": "INVOCATION"},
                            "type": "STATEMENT",
                            "lineno": 6,
                            "linenoEnd": 6,
                        },
                        {"body": "break", "type": "BREAK", "lineno": 7, "linenoEnd": 7},
                    ],
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
        tree = get_parser("switch_stmt").parse(text)
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
                    "caseKey": '"MODE_1"',
                    "type": "CASE",
                    "lineno": 3,
                    "linenoEnd": 6,
                    "body": [
                        {
                            "body": {"name": "doSomething", "type": "INVOCATION"},
                            "type": "STATEMENT",
                            "lineno": 4,
                            "linenoEnd": 4,
                        },
                        {
                            "body": {"name": "doSomething", "type": "INVOCATION"},
                            "type": "STATEMENT",
                            "lineno": 5,
                            "linenoEnd": 5,
                        },
                        {"body": "break", "type": "BREAK", "lineno": 6, "linenoEnd": 6},
                    ],
                },
                {
                    "caseKey": '"MODE_2"',
                    "type": "CASE",
                    "lineno": 7,
                    "linenoEnd": 9,
                    "body": [
                        {
                            "body": {"name": "doSomething", "type": "INVOCATION"},
                            "type": "STATEMENT",
                            "lineno": 8,
                            "linenoEnd": 8,
                        },
                        {"body": "break", "type": "BREAK", "lineno": 9, "linenoEnd": 9},
                    ],
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
        tree = get_parser("switch_stmt").parse(text)
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
                    "caseKey": "default",
                    "type": "CASE",
                    "lineno": 3,
                    "linenoEnd": 5,
                    "body": [
                        {
                            "body": {"name": "doNothing", "type": "INVOCATION"},
                            "type": "STATEMENT",
                            "lineno": 4,
                            "linenoEnd": 4,
                        },
                        {"body": "break", "type": "BREAK", "lineno": 5, "linenoEnd": 5},
                    ],
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
                    "caseKey": "default",
                    "type": "CASE",
                    "lineno": 2,
                    "linenoEnd": 6,
                    "body": [
                        {
                            "body": {"name": "doNothing", "type": "INVOCATION"},
                            "type": "STATEMENT",
                            "lineno": 3,
                            "linenoEnd": 3,
                        },
                        {
                            "body": {"name": "doNothing", "type": "INVOCATION"},
                            "type": "STATEMENT",
                            "lineno": 4,
                            "linenoEnd": 4,
                        },
                        {
                            "body": {"name": "doNothing", "type": "INVOCATION"},
                            "type": "STATEMENT",
                            "lineno": 5,
                            "linenoEnd": 5,
                        },
                        {"body": "break", "type": "BREAK", "lineno": 6, "linenoEnd": 6},
                    ],
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
                {"caseKey": "ABC", "type": "CASE", "lineno": 2, "linenoEnd": 2},
                {
                    "caseKey": "default",
                    "type": "CASE",
                    "lineno": 3,
                    "linenoEnd": 7,
                    "body": [
                        {
                            "body": {"name": "doNothing", "type": "INVOCATION"},
                            "type": "STATEMENT",
                            "lineno": 4,
                            "linenoEnd": 4,
                        },
                        {
                            "body": {"name": "doNothing", "type": "INVOCATION"},
                            "type": "STATEMENT",
                            "lineno": 5,
                            "linenoEnd": 5,
                        },
                        {
                            "body": {"name": "doNothing", "type": "INVOCATION"},
                            "type": "STATEMENT",
                            "lineno": 6,
                            "linenoEnd": 6,
                        },
                        {"body": "break", "type": "BREAK", "lineno": 7, "linenoEnd": 7},
                    ],
                },
            ],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_switch_case8(self):

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
        tree = get_parser("stmt", parser="earley").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {
            "test": "mode",
            "type": "SWITCH",
            "lineno": 1,
            "linenoEnd": 10,
            "cases": [
                {
                    "caseKey": "ABC",
                    "type": "CASE",
                    "lineno": 2,
                    "linenoEnd": 4,
                    "body": [
                        {
                            "body": {"name": "doNothing", "type": "INVOCATION"},
                            "type": "STATEMENT",
                            "lineno": 3,
                            "linenoEnd": 3,
                        },
                        {"body": "break", "type": "BREAK", "lineno": 4, "linenoEnd": 4},
                    ],
                },
                {
                    "caseKey": "default",
                    "type": "CASE",
                    "lineno": 5,
                    "linenoEnd": 9,
                    "body": [
                        {
                            "body": {"name": "doNothing", "type": "INVOCATION"},
                            "type": "STATEMENT",
                            "lineno": 6,
                            "linenoEnd": 6,
                        },
                        {
                            "body": {"name": "doNothing", "type": "INVOCATION"},
                            "type": "STATEMENT",
                            "lineno": 7,
                            "linenoEnd": 7,
                        },
                        {
                            "body": {"name": "doNothing", "type": "INVOCATION"},
                            "type": "STATEMENT",
                            "lineno": 8,
                            "linenoEnd": 8,
                        },
                        {"body": "break", "type": "BREAK", "lineno": 9, "linenoEnd": 9},
                    ],
                },
            ],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_switch_case9(self):

        text = """switch(mode){
                case "MODE_1":
                    doSomething();
                    break;
                case "MODE_2":
                case "MODE_3":
                default:
                    doAnotherThing();
                    break;
            }"""
        tree = get_parser("stmt", parser="earley").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {
            "test": "mode",
            "type": "SWITCH",
            "lineno": 1,
            "linenoEnd": 10,
            "cases": [
                {
                    "caseKey": '"MODE_1"',
                    "type": "CASE",
                    "lineno": 2,
                    "linenoEnd": 4,
                    "body": [
                        {
                            "body": {"name": "doSomething", "type": "INVOCATION"},
                            "type": "STATEMENT",
                            "lineno": 3,
                            "linenoEnd": 3,
                        },
                        {"body": "break", "type": "BREAK", "lineno": 4, "linenoEnd": 4},
                    ],
                },
                {"caseKey": '"MODE_2"', "type": "CASE", "lineno": 5, "linenoEnd": 5},
                {"caseKey": '"MODE_3"', "type": "CASE", "lineno": 6, "linenoEnd": 6},
                {
                    "caseKey": "default",
                    "type": "CASE",
                    "lineno": 7,
                    "linenoEnd": 9,
                    "body": [
                        {
                            "body": {"name": "doAnotherThing", "type": "INVOCATION"},
                            "type": "STATEMENT",
                            "lineno": 8,
                            "linenoEnd": 8,
                        },
                        {"body": "break", "type": "BREAK", "lineno": 9, "linenoEnd": 9},
                    ],
                },
            ],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_switch_case10(self):

        text = """switch (name.method()) {
                        case other.CASE_KEY:
                            util
                                .handleError(err, ErrId.E123);
                            break;
                    }"""
        tree = get_parser("stmt", parser="earley").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {
            "test": {"name": "name.method", "type": "INVOCATION"},
            "type": "SWITCH",
            "lineno": 1,
            "linenoEnd": 6,
            "cases": [
                {
                    "caseKey": "other.CASE_KEY",
                    "type": "CASE",
                    "lineno": 2,
                    "linenoEnd": 5,
                    "body": [
                        {
                            "body": {
                                "name": "util.handleError",
                                "type": "INVOCATION",
                                "args": ["err", "ErrId.E123"],
                            },
                            "type": "STATEMENT",
                            "lineno": 3,
                            "linenoEnd": 4,
                        },
                        {"body": "break", "type": "BREAK", "lineno": 5, "linenoEnd": 5},
                    ],
                }
            ],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_for_case1(self):

        text = """
        for (int i = 0; i <= 10; i++) {
            doSomething();
        }
        """
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {
            "test": {
                "variable": {
                    "name": "i",
                    "assign": 0.0,
                    "classType": "int",
                    "type": "STATEMENT",
                    "lineno": 2,
                    "linenoEnd": 2,
                },
                "test": {
                    "left": "i",
                    "chain": [{"value": 10.0, "operator": "<="}],
                    "type": "COMPARISON",
                },
                "expr": {
                    "value": "i",
                    "operator": "++",
                    "type": "BINARY_AFTER_EXPRESSION",
                },
                "type": "FOR_LOOP_TEST",
            },
            "type": "FOR_LOOP",
            "lineno": 2,
            "linenoEnd": 4,
            "body": [
                {
                    "body": {"name": "doSomething", "type": "INVOCATION"},
                    "type": "STATEMENT",
                    "lineno": 3,
                    "linenoEnd": 3,
                }
            ],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_for_case2(self):

        text = """
        for (int i : intArray) {
            doSomething();
            continue;
        }
        """
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {
            "test": {
                "variable": "i",
                "classType": "int",
                "list": "intArray",
                "type": "FOR_EACH_TEST",
            },
            "type": "FOR_LOOP",
            "lineno": 2,
            "linenoEnd": 5,
            "body": [
                {
                    "body": {"name": "doSomething", "type": "INVOCATION"},
                    "type": "STATEMENT",
                    "lineno": 3,
                    "linenoEnd": 3,
                },
                {"body": "continue", "type": "CONTINUE", "lineno": 4, "linenoEnd": 4},
            ],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_while_case1(self):

        text = """
        while (flag) {
            doSomething();
        }
        """
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {
            "test": "flag",
            "type": "WHILE_LOOP",
            "lineno": 2,
            "linenoEnd": 4,
            "body": [
                {
                    "body": {"name": "doSomething", "type": "INVOCATION"},
                    "type": "STATEMENT",
                    "lineno": 3,
                    "linenoEnd": 3,
                }
            ],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_do_while_case1(self):

        text = """
        do {
            doSomething();
        } while (flag)
        """
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {
            "test": "flag",
            "type": "DO_WHILE_LOOP",
            "lineno": 2,
            "linenoEnd": 4,
            "body": [
                {
                    "body": {"name": "doSomething", "type": "INVOCATION"},
                    "type": "STATEMENT",
                    "lineno": 3,
                    "linenoEnd": 3,
                }
            ],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_try_case1(self):

        text = """
        try {
            doSomething();
        }
        """
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {
            "type": "TRY",
            "lineno": 2,
            "linenoEnd": 4,
            "body": [
                {
                    "body": {"name": "doSomething", "type": "INVOCATION"},
                    "type": "STATEMENT",
                    "lineno": 3,
                    "linenoEnd": 3,
                }
            ],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_try_case2(self):

        text = """
        try (Resource r = getResource()) {
            doSomething();
        }
        """
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {
            "type": "TRY",
            "lineno": 2,
            "linenoEnd": 4,
            "body": [
                {
                    "body": {"name": "doSomething", "type": "INVOCATION"},
                    "type": "STATEMENT",
                    "lineno": 3,
                    "linenoEnd": 3,
                }
            ],
            "with": {
                "name": "r",
                "assign": {"name": "getResource", "type": "INVOCATION"},
                "classType": "Resource",
                "type": "STATEMENT",
                "lineno": 2,
                "linenoEnd": 2,
            },
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_try_case3(self):

        text = """
        try (Resource r = getResource()) {
            doSomething();
        } catch (Exception ex) {
            doSomethingElse();
        }
        """
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {
            "type": "TRY",
            "lineno": 2,
            "linenoEnd": 6,
            "catches": [
                {
                    "exceptions": [
                        {"name": "ex", "classType": "Exception", "type": "PARAMETER"}
                    ],
                    "type": "CATCH",
                    "lineno": 4,
                    "linenoEnd": 6,
                    "body": [
                        {
                            "body": {"name": "doSomethingElse", "type": "INVOCATION"},
                            "type": "STATEMENT",
                            "lineno": 5,
                            "linenoEnd": 5,
                        }
                    ],
                }
            ],
            "body": [
                {
                    "body": {"name": "doSomething", "type": "INVOCATION"},
                    "type": "STATEMENT",
                    "lineno": 3,
                    "linenoEnd": 3,
                }
            ],
            "with": {
                "name": "r",
                "assign": {"name": "getResource", "type": "INVOCATION"},
                "classType": "Resource",
                "type": "STATEMENT",
                "lineno": 2,
                "linenoEnd": 2,
            },
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_try_case4(self):

        text = """
        try (Resource r = getResource()) {
            doSomething();
        } catch (Exception ex | Error err) {
            doSomethingElse();
        } finally {
            nothing();
        }
        """
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {
            "type": "TRY",
            "lineno": 2,
            "linenoEnd": 8,
            "catches": [
                {
                    "exceptions": [
                        {"name": "ex", "classType": "Exception", "type": "PARAMETER"},
                        {"name": "err", "classType": "Error", "type": "PARAMETER"},
                    ],
                    "type": "CATCH",
                    "lineno": 4,
                    "linenoEnd": 6,
                    "body": [
                        {
                            "body": {"name": "doSomethingElse", "type": "INVOCATION"},
                            "type": "STATEMENT",
                            "lineno": 5,
                            "linenoEnd": 5,
                        }
                    ],
                }
            ],
            "finally": {
                "type": "FINALLY",
                "lineno": 6,
                "linenoEnd": 8,
                "body": [
                    {
                        "body": {"name": "nothing", "type": "INVOCATION"},
                        "type": "STATEMENT",
                        "lineno": 7,
                        "linenoEnd": 7,
                    }
                ],
            },
            "body": [
                {
                    "body": {"name": "doSomething", "type": "INVOCATION"},
                    "type": "STATEMENT",
                    "lineno": 3,
                    "linenoEnd": 3,
                }
            ],
            "with": {
                "name": "r",
                "assign": {"name": "getResource", "type": "INVOCATION"},
                "classType": "Resource",
                "type": "STATEMENT",
                "lineno": 2,
                "linenoEnd": 2,
            },
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_try_case5(self):

        text = """
        try (Resource r = getResource()) {
            doSomething();
        } catch (Exception ex | Error err) {
            doSomethingElse();
        } catch (Exception ex2 | Error err2) {
            doSomethingElse();
        } finally {
            no();
        }
        """
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {
            "type": "TRY",
            "lineno": 2,
            "linenoEnd": 10,
            "catches": [
                {
                    "exceptions": [
                        {"name": "ex", "classType": "Exception", "type": "PARAMETER"},
                        {"name": "err", "classType": "Error", "type": "PARAMETER"},
                    ],
                    "type": "CATCH",
                    "lineno": 4,
                    "linenoEnd": 6,
                    "body": [
                        {
                            "body": {"name": "doSomethingElse", "type": "INVOCATION"},
                            "type": "STATEMENT",
                            "lineno": 5,
                            "linenoEnd": 5,
                        }
                    ],
                },
                {
                    "exceptions": [
                        {"name": "ex2", "classType": "Exception", "type": "PARAMETER"},
                        {"name": "err2", "classType": "Error", "type": "PARAMETER"},
                    ],
                    "type": "CATCH",
                    "lineno": 6,
                    "linenoEnd": 8,
                    "body": [
                        {
                            "body": {"name": "doSomethingElse", "type": "INVOCATION"},
                            "type": "STATEMENT",
                            "lineno": 7,
                            "linenoEnd": 7,
                        }
                    ],
                },
            ],
            "finally": {
                "type": "FINALLY",
                "lineno": 8,
                "linenoEnd": 10,
                "body": [
                    {
                        "body": {"name": "no", "type": "INVOCATION"},
                        "type": "STATEMENT",
                        "lineno": 9,
                        "linenoEnd": 9,
                    }
                ],
            },
            "body": [
                {
                    "body": {"name": "doSomething", "type": "INVOCATION"},
                    "type": "STATEMENT",
                    "lineno": 3,
                    "linenoEnd": 3,
                }
            ],
            "with": {
                "name": "r",
                "assign": {"name": "getResource", "type": "INVOCATION"},
                "classType": "Resource",
                "type": "STATEMENT",
                "lineno": 2,
                "linenoEnd": 2,
            },
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_try_case6(self):

        text = """
        try {
            doSomething();
        } catch (Exception ex | Error err) {
            doSomethingElse();
        } catch (Exception ex2 | Error err2) {
            doSomethingElse();
        } finally {
            no();
        }
        """
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {
            "type": "TRY",
            "lineno": 2,
            "linenoEnd": 10,
            "catches": [
                {
                    "exceptions": [
                        {"name": "ex", "classType": "Exception", "type": "PARAMETER"},
                        {"name": "err", "classType": "Error", "type": "PARAMETER"},
                    ],
                    "type": "CATCH",
                    "lineno": 4,
                    "linenoEnd": 6,
                    "body": [
                        {
                            "body": {"name": "doSomethingElse", "type": "INVOCATION"},
                            "type": "STATEMENT",
                            "lineno": 5,
                            "linenoEnd": 5,
                        }
                    ],
                },
                {
                    "exceptions": [
                        {"name": "ex2", "classType": "Exception", "type": "PARAMETER"},
                        {"name": "err2", "classType": "Error", "type": "PARAMETER"},
                    ],
                    "type": "CATCH",
                    "lineno": 6,
                    "linenoEnd": 8,
                    "body": [
                        {
                            "body": {"name": "doSomethingElse", "type": "INVOCATION"},
                            "type": "STATEMENT",
                            "lineno": 7,
                            "linenoEnd": 7,
                        }
                    ],
                },
            ],
            "finally": {
                "type": "FINALLY",
                "lineno": 8,
                "linenoEnd": 10,
                "body": [
                    {
                        "body": {"name": "no", "type": "INVOCATION"},
                        "type": "STATEMENT",
                        "lineno": 9,
                        "linenoEnd": 9,
                    }
                ],
            },
            "body": [
                {
                    "body": {"name": "doSomething", "type": "INVOCATION"},
                    "type": "STATEMENT",
                    "lineno": 3,
                    "linenoEnd": 3,
                }
            ],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_lambda_case1(self):

        text = """
        args -> {

			System.out.println("Let's inspect the beans provided by Spring Boot:");

			String[] beanNames = ctx.getBeanDefinitionNames();
			Arrays.sort(beanNames);
			for (String beanName : beanNames) {
				System.out.println(beanName);
			}

		}
        """
        tree = get_parser("test").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {
            "parameters": ["args"],
            "body": [
                {
                    "body": {
                        "name": "System.out.println",
                        "type": "INVOCATION",
                        "args": ['"Let\'s inspect the beans provided by Spring Boot:"'],
                    },
                    "type": "STATEMENT",
                    "lineno": 4,
                    "linenoEnd": 4,
                },
                {
                    "name": "beanNames",
                    "assign": {
                        "name": "ctx.getBeanDefinitionNames",
                        "type": "INVOCATION",
                    },
                    "classType": {"name": "String", "arraySuffix": "[]"},
                    "type": "STATEMENT",
                    "lineno": 6,
                    "linenoEnd": 6,
                },
                {
                    "body": {
                        "name": "Arrays.sort",
                        "type": "INVOCATION",
                        "args": ["beanNames"],
                    },
                    "type": "STATEMENT",
                    "lineno": 7,
                    "linenoEnd": 7,
                },
                {
                    "test": {
                        "variable": "beanName",
                        "classType": "String",
                        "list": "beanNames",
                        "type": "FOR_EACH_TEST",
                    },
                    "type": "FOR_LOOP",
                    "lineno": 8,
                    "linenoEnd": 10,
                    "body": [
                        {
                            "body": {
                                "name": "System.out.println",
                                "type": "INVOCATION",
                                "args": ["beanName"],
                            },
                            "type": "STATEMENT",
                            "lineno": 9,
                            "linenoEnd": 9,
                        }
                    ],
                },
            ],
            "type": "LAMBDA_EXPRESSION",
            "lineno": 2,
            "linenoEnd": 12,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_lambda_case2(self):

        text = """
        parameter -> parameter + " from lambda"
        """
        tree = get_parser("test").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {
            "parameters": ["parameter"],
            "body": [
                {
                    "body": {
                        "left": "parameter",
                        "chain": [{"value": '" from lambda"', "operator": "+"}],
                        "type": "ARITHMETIC_EXPRESSION",
                    },
                    "type": "STATEMENT",
                    "lineno": 2,
                    "linenoEnd": 2,
                }
            ],
            "type": "LAMBDA_EXPRESSION",
            "lineno": 2,
            "linenoEnd": 2,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_lambda_case3(self):

        text = """
        (int x)->System.out.println(2*x)
        """
        tree = get_parser("test").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {
            "parameters": [{"name": "x", "classType": "int", "type": "PARAMETER"}],
            "body": [
                {
                    "body": {
                        "name": "System.out.println",
                        "type": "INVOCATION",
                        "args": [
                            {
                                "left": 2.0,
                                "chain": [{"value": "x", "operator": "*"}],
                                "type": "ARITHMETIC_EXPRESSION",
                            }
                        ],
                    },
                    "type": "STATEMENT",
                    "lineno": 2,
                    "linenoEnd": 2,
                }
            ],
            "type": "LAMBDA_EXPRESSION",
            "lineno": 2,
            "linenoEnd": 2,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_lambda_case4(self):

        text = """
        () -> System.out.println("Print somthing!")
        """
        tree = get_parser("test").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {
            "body": [
                {
                    "body": {
                        "name": "System.out.println",
                        "type": "INVOCATION",
                        "args": ['"Print somthing!"'],
                    },
                    "type": "STATEMENT",
                    "lineno": 2,
                    "linenoEnd": 2,
                }
            ],
            "type": "LAMBDA_EXPRESSION",
            "lineno": 2,
            "linenoEnd": 2,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_list_literal_case1(self):

        text = "String[] list = {STR_1, STR_2, STR_3};"
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {
            "name": "list",
            "assign": ["STR_1", "STR_2", "STR_3"],
            "classType": {"name": "String", "arraySuffix": "[]"},
            "type": "STATEMENT",
            "lineno": 1,
            "linenoEnd": 1,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_list_literal_case2(self):

        text = "new String[]{STR_1, STR_2, STR_3};"
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {
            "body": {
                "value": {
                    "name": {"name": "String", "arraySuffix": "[]"},
                    "type": "ARRAY_LITERAL",
                    "value": ["STR_1", "STR_2", "STR_3"],
                },
                "type": "NEW_EXPRESSION",
            },
            "type": "STATEMENT",
            "lineno": 1,
            "linenoEnd": 1,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_special_case1(self):

        text = "name;;"
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = TestMethodTransformer().transform(tree)
        print(result)
        expected = {"body": "name", "type": "STATEMENT", "lineno": 1, "linenoEnd": 1}
        self.assertEqual(result, expected, "Not matched.")

