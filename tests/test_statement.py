import unittest
from tests.helper import get_parser
from java_parser.enum import EnumTransformer
from java_parser.method import MethodTransformer
from java_parser.common import CommonTransformer
from java_parser.clazz import ClassTransformer


class CompoundMethodTransformer(
    CommonTransformer, ClassTransformer, MethodTransformer, EnumTransformer
):
    pass


class TestStatement(unittest.TestCase):
    def test_stmt_case1(self):

        text = "break;"
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {"body": "break", "type": "BREAK", "lineno": 1, "linenoEnd": 1}
        self.assertEqual(result, expected, "Not matched.")

    def test_stmt_case2(self):

        text = "continue;"
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {"body": "continue", "type": "CONTINUE", "lineno": 1, "linenoEnd": 1}
        self.assertEqual(result, expected, "Not matched.")

    def test_stmt_case3(self):

        text = "return;"
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {"body": "return", "type": "RETURN", "lineno": 1, "linenoEnd": 1}
        self.assertEqual(result, expected, "Not matched.")

    def test_stmt_case4(self):

        text = "return something(args);"
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
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
        result = CompoundMethodTransformer().transform(tree)
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
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "name": "name",
            "assign": '"Real Name"',
            "operator": "=",
            "classType": "String",
            "modifiers": ["private", "static"],
            "type": "ASSIGNMENT",
            "lineno": 1,
            "linenoEnd": 1,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_stmt_case7(self):

        text = "int thisNumber = self++;"
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "classType": "int",
            "name": "thisNumber",
            "assign": {
                "value": "self",
                "operator": "++",
                "type": "BINARY_AFTER_EXPRESSION",
            },
            "operator": "=",
            "type": "ASSIGNMENT",
            "lineno": 1,
            "linenoEnd": 1,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_stmt_case8(self):

        text = "String name = (String) SomeVariable.attribute;"
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "classType": "String",
            "name": "name",
            "assign": {
                "value": "SomeVariable.attribute",
                "cast": "String",
                "type": "CAST_EXPRESSION",
            },
            "operator": "=",
            "type": "ASSIGNMENT",
            "lineno": 1,
            "linenoEnd": 1,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_stmt_case9(self):

        text = "String name = (ArrayList<String>)SomeVariable.attribute;"
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "name": "name",
            "assign": {
                "value": "SomeVariable.attribute",
                "cast": {"name": "ArrayList", "generic": ["String"]},
                "type": "CAST_EXPRESSION",
            },
            "operator": "=",
            "classType": "String",
            "type": "ASSIGNMENT",
            "lineno": 1,
            "linenoEnd": 1,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_stmt_case10(self):

        text = "return sb2.toString() + WHERE_START + sb.toString() + WHERE_END;"
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
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
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "type": "INVOCATION",
            "name": "assertThat",
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
            "lineno": 1,
            "linenoEnd": 1,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_stmt_case12(self):

        text = "doSomeThingHere(Parameter);"
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "type": "INVOCATION",
            "name": "doSomeThingHere",
            "args": ["Parameter"],
            "lineno": 1,
            "linenoEnd": 1,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_stmt_case13(self):

        text = "(SomeType)doSomeThingHere(Parameter).doSomething();"
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "type": "CAST_EXPRESSION",
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
            "lineno": 1,
            "linenoEnd": 1,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_stmt_case14(self):

        text = "object = factory.makeObject(param);"
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "name": "object",
            "assign": {
                "name": "factory.makeObject",
                "type": "INVOCATION",
                "args": ["param"],
            },
            "operator": "=",
            "type": "ASSIGNMENT",
            "lineno": 1,
            "linenoEnd": 1,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_stmt_case15(self):

        text = "assert key != null;"
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "type": "ASSERT",
            "body": {
                "left": "key",
                "chain": [{"value": None, "operator": "!="}],
                "type": "COMPARISON",
            },
            "lineno": 1,
            "linenoEnd": 1,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_stmt_case16(self):

        text = """
        someInt += Integer.parseInt(Object.get(Constant.NUMBER_0, ins.getAnother()));
        """
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "name": "someInt",
            "assign": {
                "name": "Integer.parseInt",
                "type": "INVOCATION",
                "args": [
                    {
                        "name": "Object.get",
                        "type": "INVOCATION",
                        "args": [
                            "Constant.NUMBER_0",
                            {"name": "ins.getAnother", "type": "INVOCATION"},
                        ],
                    }
                ],
            },
            "operator": "+=",
            "type": "ASSIGNMENT",
            "lineno": 2,
            "linenoEnd": 2,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_stmt_case17(self):

        text = """
        String str[];
        """
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "body": {"name": "str", "arraySuffix": "[]", "type": "ARRAY_LITERAL_NAME"},
            "classType": "String",
            "type": "STATEMENT",
            "lineno": 2,
            "linenoEnd": 2,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_stmt_case18(self):

        text = """
        wtf;;
        """
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {"body": "wtf", "type": "STATEMENT", "lineno": 2, "linenoEnd": 2}
        self.assertEqual(result, expected, "Not matched.")

    def test_stmt_case19(self):

        text = """
        wtf; ;
        """
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {"body": "wtf", "type": "STATEMENT", "lineno": 2, "linenoEnd": 2}
        self.assertEqual(result, expected, "Not matched.")

    def test_stmt_case20(self):

        text = """
        this.name = "Real Name";
        """
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "type": "ASSIGNMENT",
            "name": "this.name",
            "assign": '"Real Name"',
            "operator": "=",
            "lineno": 2,
            "linenoEnd": 2,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_stmt_case21(self):

        text = """
        arr[i] = "Real Name";
        """
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "type": "ASSIGNMENT",
            "name": {"name": "arr", "index": "i", "type": "ARRAY_OPERATION"},
            "assign": '"Real Name"',
            "operator": "=",
            "lineno": 2,
            "linenoEnd": 2,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_stmt_case22(self):

        text = """
        arr[i + 1] = "Real Name";
        """
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "type": "ASSIGNMENT",
            "name": {
                "name": "arr",
                "index": {
                    "left": "i",
                    "chain": [{"value": 1, "operator": "+"}],
                    "type": "ARITHMETIC_EXPRESSION",
                },
                "type": "ARRAY_OPERATION",
            },
            "assign": '"Real Name"',
            "operator": "=",
            "lineno": 2,
            "linenoEnd": 2,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_stmt_case23(self):

        text = """
        this.arr[i + 1] = "Real Name";
        """
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "type": "ASSIGNMENT",
            "name": {
                "name": "this.arr",
                "index": {
                    "left": "i",
                    "chain": [{"value": 1, "operator": "+"}],
                    "type": "ARITHMETIC_EXPRESSION",
                },
                "type": "ARRAY_OPERATION",
            },
            "assign": '"Real Name"',
            "operator": "=",
            "lineno": 2,
            "linenoEnd": 2,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_stmt_case24(self):

        text = """
        String[] arr = {};
        """
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "type": "ASSIGNMENT",
            "name": "arr",
            "assign": "{}",
            "operator": "=",
            "classType": {"name": "String", "arraySuffix": "[]"},
            "lineno": 2,
            "linenoEnd": 2,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_stmt_case25(self):

        text = """
        int x = 1,
            y = 2,
            z = 3, a, b, c, d;
        """
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "type": "ASSIGNMENT_MULTIPLE",
            "value": [
                {"name": "x", "assign": 1, "operator": "=", "type": "ASSIGNMENT"},
                {"name": "y", "assign": 2, "operator": "=", "type": "ASSIGNMENT"},
                {"name": "z", "assign": 3, "operator": "=", "type": "ASSIGNMENT"},
                {"body": "a", "type": "DECLARATION"},
                {"body": "b", "type": "DECLARATION"},
                {"body": "c", "type": "DECLARATION"},
                {"body": "d", "type": "DECLARATION"},
            ],
            "classType": "int",
            "lineno": 2,
            "linenoEnd": 4,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_stmt_case26(self):

        text = """
        ClassType cl = new AnonymousType() {
            public void doSomething() {
                action();
            }
        };
        """
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "type": "ASSIGNMENT",
            "name": "cl",
            "assign": {
                "name": "AnonymousType",
                "methods": [
                    {
                        "name": "doSomething",
                        "body": [
                            {
                                "type": "INVOCATION",
                                "name": "action",
                                "lineno": 4,
                                "linenoEnd": 4,
                            }
                        ],
                        "returnType": "void",
                        "type": "METHOD",
                        "modifiers": ["public"],
                        "lineno": 3,
                        "linenoEnd": 5,
                    }
                ],
                "type": "ANONYMOUS_CLASS",
                "lineno": 2,
                "linenoEnd": 6,
            },
            "operator": "=",
            "classType": "ClassType",
            "lineno": 2,
            "linenoEnd": 6,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_stmt_case27(self):

        text = """
        ClassType cl = new AnonymousType() {
            public void doSomething() {
                action();
            }
        };
        """
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "type": "ASSIGNMENT",
            "name": "cl",
            "assign": {
                "name": "AnonymousType",
                "methods": [
                    {
                        "name": "doSomething",
                        "body": [
                            {
                                "type": "INVOCATION",
                                "name": "action",
                                "lineno": 4,
                                "linenoEnd": 4,
                            }
                        ],
                        "returnType": "void",
                        "type": "METHOD",
                        "modifiers": ["public"],
                        "lineno": 3,
                        "linenoEnd": 5,
                    }
                ],
                "type": "ANONYMOUS_CLASS",
                "lineno": 2,
                "linenoEnd": 6,
            },
            "operator": "=",
            "classType": "ClassType",
            "lineno": 2,
            "linenoEnd": 6,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_stmt_case28(self):

        text = """
        synchronized (lock) {
            action();
        };
        """
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "target": "lock",
            "body": [
                {"type": "INVOCATION", "name": "action", "lineno": 3, "linenoEnd": 3}
            ],
            "type": "SYNCHRONIZED",
            "lineno": 2,
            "linenoEnd": 4,
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
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = [
            {
                "type": "INVOCATION",
                "name": "doSomeThingHere",
                "args": ["Parameter"],
                "lineno": 2,
                "linenoEnd": 2,
            },
            {
                "type": "INVOCATION",
                "name": "doSomeThingHere",
                "args": ["Parameter"],
                "lineno": 3,
                "linenoEnd": 3,
            },
            {
                "type": "INVOCATION",
                "name": "doSomeThingHere",
                "args": ["Parameter"],
                "lineno": 4,
                "linenoEnd": 4,
            },
            {
                "type": "INVOCATION",
                "name": "doSomeThingHere",
                "args": ["Parameter"],
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
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = [
            {
                "type": "IF",
                "test": "someConditions",
                "lineno": 2,
                "linenoEnd": 8,
                "body": [
                    {
                        "type": "INVOCATION",
                        "name": "doSomeThingHere",
                        "args": ["Parameter"],
                        "lineno": 3,
                        "linenoEnd": 3,
                    },
                    {
                        "type": "INVOCATION",
                        "name": "doSomeThingHere",
                        "args": ["Parameter"],
                        "lineno": 4,
                        "linenoEnd": 4,
                    },
                    {
                        "type": "INVOCATION",
                        "name": "doSomeThingHere",
                        "args": ["Parameter"],
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
                                "type": "INVOCATION",
                                "name": "maybeSomeCleanUpHere",
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
                        "type": "INVOCATION",
                        "name": "doSomeThingHere",
                        "args": ["Parameter"],
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
                                "type": "INVOCATION",
                                "name": "maybeSomeCleanUpHere",
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
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = [
            {
                "type": "IF",
                "test": "someConditions",
                "lineno": 2,
                "linenoEnd": 6,
                "body": [
                    {
                        "type": "INVOCATION",
                        "name": "doSomeThingHere1",
                        "args": ["Parameter"],
                        "lineno": 3,
                        "linenoEnd": 3,
                    },
                    {
                        "type": "INVOCATION",
                        "name": "doSomeThingHere2",
                        "args": ["Parameter"],
                        "lineno": 4,
                        "linenoEnd": 4,
                    },
                    {
                        "type": "INVOCATION",
                        "name": "doSomeThingHere3",
                        "args": ["Parameter"],
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
                        "type": "INVOCATION",
                        "name": "doSomeThingHere",
                        "args": ["Parameter"],
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
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "type": "IF",
            "test": "someConditions",
            "lineno": 2,
            "linenoEnd": 4,
            "body": [
                {
                    "type": "INVOCATION",
                    "name": "doSomeThingHere",
                    "args": ["Parameter"],
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
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "type": "IF",
            "test": "someConditions",
            "lineno": 2,
            "linenoEnd": 8,
            "body": [
                {
                    "type": "INVOCATION",
                    "name": "doSomeThingHere",
                    "args": ["Parameter"],
                    "lineno": 3,
                    "linenoEnd": 3,
                },
                {
                    "type": "INVOCATION",
                    "name": "doSomeThingHere",
                    "args": ["Parameter"],
                    "lineno": 4,
                    "linenoEnd": 4,
                },
                {
                    "type": "INVOCATION",
                    "name": "doSomeThingHere",
                    "args": ["Parameter"],
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
                            "type": "INVOCATION",
                            "name": "maybeSomeCleanUpHere",
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
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "type": "IF",
            "test": "someConditions",
            "lineno": 2,
            "linenoEnd": 12,
            "body": [
                {
                    "type": "INVOCATION",
                    "name": "doSomeThingHere",
                    "args": ["Parameter"],
                    "lineno": 3,
                    "linenoEnd": 3,
                },
                {
                    "type": "INVOCATION",
                    "name": "doSomeThingHere",
                    "args": ["Parameter"],
                    "lineno": 4,
                    "linenoEnd": 4,
                },
                {
                    "type": "INVOCATION",
                    "name": "doSomeThingHere",
                    "args": ["Parameter"],
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
                            "type": "INVOCATION",
                            "name": "doOtherThingHere",
                            "args": ["OtherParameter"],
                            "lineno": 7,
                            "linenoEnd": 7,
                        },
                        {
                            "type": "INVOCATION",
                            "name": "doOtherThingHere",
                            "args": ["OtherParameter"],
                            "lineno": 8,
                            "linenoEnd": 8,
                        },
                        {
                            "type": "INVOCATION",
                            "name": "doOtherThingHere",
                            "args": ["OtherParameter"],
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
                            "type": "INVOCATION",
                            "name": "maybeSomeCleanUpHere",
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
        result = CompoundMethodTransformer().transform(tree)
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
                            "type": "INVOCATION",
                            "name": "doSomeThingHere",
                            "args": ["Parameter"],
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
                                    "type": "INVOCATION",
                                    "name": "maybeSomeCleanUpHere",
                                    "lineno": 6,
                                    "linenoEnd": 6,
                                }
                            ],
                        }
                    ],
                },
                {
                    "type": "INVOCATION",
                    "name": "doSomeThingHere",
                    "args": ["Parameter"],
                    "lineno": 8,
                    "linenoEnd": 8,
                },
                {
                    "type": "INVOCATION",
                    "name": "doSomeThingHere",
                    "args": ["Parameter"],
                    "lineno": 9,
                    "linenoEnd": 9,
                },
                {
                    "type": "INVOCATION",
                    "name": "doSomeThingHere",
                    "args": ["Parameter"],
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
                            "type": "INVOCATION",
                            "name": "maybeSomeCleanUpHere",
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
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "type": "IF",
            "test": "someConditions",
            "lineno": 2,
            "linenoEnd": 7,
            "body": [
                {
                    "type": "INVOCATION",
                    "name": "doSomeThingHere1",
                    "args": ["Parameter"],
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
                            "type": "INVOCATION",
                            "name": "doSomeThingHere2",
                            "args": ["Parameter"],
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
                            "type": "INVOCATION",
                            "name": "doSomeThingHere3",
                            "args": ["Parameter"],
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
        result = CompoundMethodTransformer().transform(tree)
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
                {"type": "INVOCATION", "name": "something", "lineno": 3, "linenoEnd": 3}
            ],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_if_case7(self):

        text = """
        /** Test 1 */
        if (!obj.equals(Other.CONSTANTS_1)) {
            target.doSomething(obj.format(param));
        }
        /** Test 2 */
        if (!another.equals("string")) {
            target.doMoreThing(obj.get(name));
        }
        """
        tree = get_parser("suit").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = [
            {
                "type": "IF",
                "test": {
                    "value": {
                        "name": "obj.equals",
                        "type": "INVOCATION",
                        "args": ["Other.CONSTANTS_1"],
                    },
                    "type": "TEST_NOT",
                },
                "lineno": 2,
                "linenoEnd": 5,
                "body": [
                    {
                        "type": "INVOCATION",
                        "name": "target.doSomething",
                        "args": [
                            {
                                "name": "obj.format",
                                "type": "INVOCATION",
                                "args": ["param"],
                            }
                        ],
                        "lineno": 4,
                        "linenoEnd": 4,
                    }
                ],
                "comment": ["/** Test 1 */"],
            },
            {
                "type": "IF",
                "test": {
                    "value": {
                        "name": "another.equals",
                        "type": "INVOCATION",
                        "args": ['"string"'],
                    },
                    "type": "TEST_NOT",
                },
                "lineno": 6,
                "linenoEnd": 9,
                "body": [
                    {
                        "type": "INVOCATION",
                        "name": "target.doMoreThing",
                        "args": [
                            {"name": "obj.get", "type": "INVOCATION", "args": ["name"]}
                        ],
                        "lineno": 8,
                        "linenoEnd": 8,
                    }
                ],
                "comment": ["/** Test 2 */"],
            },
        ]
        self.assertEqual(result, expected, "Not matched.")

    def test_if_case8(self):

        text = """
        if (!obj.equals(Other.CONSTANTS_1)) {
            // target.doSomething(obj.format(param));
        }
        """
        tree = get_parser("suit").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = [
            {
                "type": "IF",
                "test": {
                    "value": {
                        "name": "obj.equals",
                        "type": "INVOCATION",
                        "args": ["Other.CONSTANTS_1"],
                    },
                    "type": "TEST_NOT",
                },
                "lineno": 2,
                "linenoEnd": 4,
            }
        ]
        self.assertEqual(result, expected, "Not matched.")

    def test_switch_case1(self):

        text = """
        switch(mode) {
        }"""
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
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
        result = CompoundMethodTransformer().transform(tree)
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
        result = CompoundMethodTransformer().transform(tree)
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
                            "type": "INVOCATION",
                            "name": "doSomething",
                            "lineno": 4,
                            "linenoEnd": 4,
                        },
                        {
                            "type": "INVOCATION",
                            "name": "doSomething",
                            "lineno": 5,
                            "linenoEnd": 5,
                        },
                        {
                            "type": "INVOCATION",
                            "name": "doSomething",
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
        result = CompoundMethodTransformer().transform(tree)
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
                            "type": "INVOCATION",
                            "name": "doSomething",
                            "lineno": 4,
                            "linenoEnd": 4,
                        },
                        {
                            "type": "INVOCATION",
                            "name": "doSomething",
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
                            "type": "INVOCATION",
                            "name": "doSomething",
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
        result = CompoundMethodTransformer().transform(tree)
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
                            "type": "INVOCATION",
                            "name": "doNothing",
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
        result = CompoundMethodTransformer().transform(tree)
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
                            "type": "INVOCATION",
                            "name": "doNothing",
                            "lineno": 3,
                            "linenoEnd": 3,
                        },
                        {
                            "type": "INVOCATION",
                            "name": "doNothing",
                            "lineno": 4,
                            "linenoEnd": 4,
                        },
                        {
                            "type": "INVOCATION",
                            "name": "doNothing",
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
        result = CompoundMethodTransformer().transform(tree)
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
                            "type": "INVOCATION",
                            "name": "doNothing",
                            "lineno": 4,
                            "linenoEnd": 4,
                        },
                        {
                            "type": "INVOCATION",
                            "name": "doNothing",
                            "lineno": 5,
                            "linenoEnd": 5,
                        },
                        {
                            "type": "INVOCATION",
                            "name": "doNothing",
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
        result = CompoundMethodTransformer().transform(tree)
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
                            "type": "INVOCATION",
                            "name": "doNothing",
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
                            "type": "INVOCATION",
                            "name": "doNothing",
                            "lineno": 6,
                            "linenoEnd": 6,
                        },
                        {
                            "type": "INVOCATION",
                            "name": "doNothing",
                            "lineno": 7,
                            "linenoEnd": 7,
                        },
                        {
                            "type": "INVOCATION",
                            "name": "doNothing",
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
        result = CompoundMethodTransformer().transform(tree)
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
                            "type": "INVOCATION",
                            "name": "doSomething",
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
                            "type": "INVOCATION",
                            "name": "doAnotherThing",
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
        result = CompoundMethodTransformer().transform(tree)
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
                            "type": "INVOCATION",
                            "name": "util.handleError",
                            "args": ["err", "ErrId.E123"],
                            "lineno": 3,
                            "linenoEnd": 4,
                        },
                        {"body": "break", "type": "BREAK", "lineno": 5, "linenoEnd": 5},
                    ],
                }
            ],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_switch_case11(self):

        text = """
        /** Test 1 */
        switch(mode1) {
        }
        /** Test 2 */
        switch(mode2) {
        }
        """
        tree = get_parser("suit").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = [
            {
                "test": "mode1",
                "type": "SWITCH",
                "lineno": 2,
                "linenoEnd": 4,
                "comment": ["/** Test 1 */"],
            },
            {
                "test": "mode2",
                "type": "SWITCH",
                "lineno": 5,
                "linenoEnd": 7,
                "comment": ["/** Test 2 */"],
            },
        ]
        self.assertEqual(result, expected, "Not matched.")

    # def test_switch_case12(self):

    #     text = """
    #     switch (id) {
    #         case ID_0:
    #         case ID_1: {
    #             if (check(id, type) != constants.NO_ERROR) {
    #                 return null;
    #             }
    #             return obj.get(util.trim(type));
    #         }
    #     }
    #     """
    #     tree = get_parser("suit").parse(text)
    #     print(tree)
    #     result = CompoundMethodTransformer().transform(tree)
    #     print(result)
    #     expected = []
    #     self.assertEqual(result, expected, "Not matched.")

    def test_for_case1(self):

        text = """
        for (int i = 0; i <= 10; i++) {
            doSomething();
        }
        """
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "test": {
                "variable": {
                    "type": "ASSIGNMENT",
                    "name": "i",
                    "assign": 0,
                    "operator": "=",
                    "classType": "int",
                    "lineno": 2,
                    "linenoEnd": 2,
                },
                "test": {
                    "left": "i",
                    "chain": [{"value": 10, "operator": "<="}],
                    "type": "COMPARISON",
                },
                "type": "FOR_LOOP_TEST",
                "expr": {
                    "type": "BINARY_AFTER_EXPRESSION",
                    "value": "i",
                    "operator": "++",
                    "lineno": 2,
                    "linenoEnd": 2,
                },
            },
            "type": "FOR_LOOP",
            "lineno": 2,
            "linenoEnd": 4,
            "body": [
                {
                    "type": "INVOCATION",
                    "name": "doSomething",
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
        result = CompoundMethodTransformer().transform(tree)
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
                    "type": "INVOCATION",
                    "name": "doSomething",
                    "lineno": 3,
                    "linenoEnd": 3,
                },
                {"body": "continue", "type": "CONTINUE", "lineno": 4, "linenoEnd": 4},
            ],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_for_case3(self):

        text = """
        for (Iterator<String> iter = obj.iterator(); iter.hasNext();) {
            doSomething();
            continue;
        }
        """
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "test": {
                "variable": {
                    "type": "ASSIGNMENT",
                    "name": "iter",
                    "assign": {"name": "obj.iterator", "type": "INVOCATION"},
                    "operator": "=",
                    "classType": {"name": "Iterator", "generic": ["String"]},
                    "lineno": 2,
                    "linenoEnd": 2,
                },
                "test": {"name": "iter.hasNext", "type": "INVOCATION"},
                "type": "FOR_LOOP_TEST",
            },
            "type": "FOR_LOOP",
            "lineno": 2,
            "linenoEnd": 5,
            "body": [
                {
                    "type": "INVOCATION",
                    "name": "doSomething",
                    "lineno": 3,
                    "linenoEnd": 3,
                },
                {"body": "continue", "type": "CONTINUE", "lineno": 4, "linenoEnd": 4},
            ],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_for_case4(self):

        text = """
        /** Test 1 */
        for (int i = 0; i <= 10; i++) {
            doSomething();
        }
        /** Test 2 */
        for (int j = 0; j <= 90; j++) {
            doMore();
        }
        """
        tree = get_parser("suit").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = [
            {
                "test": {
                    "variable": {
                        "type": "ASSIGNMENT",
                        "name": "i",
                        "assign": 0,
                        "operator": "=",
                        "classType": "int",
                        "lineno": 3,
                        "linenoEnd": 3,
                    },
                    "test": {
                        "left": "i",
                        "chain": [{"value": 10, "operator": "<="}],
                        "type": "COMPARISON",
                    },
                    "type": "FOR_LOOP_TEST",
                    "expr": {
                        "type": "BINARY_AFTER_EXPRESSION",
                        "value": "i",
                        "operator": "++",
                        "lineno": 3,
                        "linenoEnd": 3,
                    },
                },
                "type": "FOR_LOOP",
                "lineno": 2,
                "linenoEnd": 5,
                "body": [
                    {
                        "type": "INVOCATION",
                        "name": "doSomething",
                        "lineno": 4,
                        "linenoEnd": 4,
                    }
                ],
                "comment": ["/** Test 1 */"],
            },
            {
                "test": {
                    "variable": {
                        "type": "ASSIGNMENT",
                        "name": "j",
                        "assign": 0,
                        "operator": "=",
                        "classType": "int",
                        "lineno": 7,
                        "linenoEnd": 7,
                    },
                    "test": {
                        "left": "j",
                        "chain": [{"value": 90, "operator": "<="}],
                        "type": "COMPARISON",
                    },
                    "type": "FOR_LOOP_TEST",
                    "expr": {
                        "type": "BINARY_AFTER_EXPRESSION",
                        "value": "j",
                        "operator": "++",
                        "lineno": 7,
                        "linenoEnd": 7,
                    },
                },
                "type": "FOR_LOOP",
                "lineno": 6,
                "linenoEnd": 9,
                "body": [
                    {
                        "type": "INVOCATION",
                        "name": "doMore",
                        "lineno": 8,
                        "linenoEnd": 8,
                    }
                ],
                "comment": ["/** Test 2 */"],
            },
        ]
        self.assertEqual(result, expected, "Not matched.")

    def test_for_case5(self):

        text = """
        for (int j = 0, i = 0; j <= 90; j++, i++) {
            action();
        }
        """
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "test": {
                "variable": {
                    "type": "ASSIGNMENT_MULTIPLE",
                    "value": [
                        {
                            "name": "j",
                            "assign": 0,
                            "operator": "=",
                            "type": "ASSIGNMENT",
                        },
                        {
                            "name": "i",
                            "assign": 0,
                            "operator": "=",
                            "type": "ASSIGNMENT",
                        },
                    ],
                    "classType": "int",
                    "lineno": 2,
                    "linenoEnd": 2,
                },
                "test": {
                    "left": "j",
                    "chain": [{"value": 90, "operator": "<="}],
                    "type": "COMPARISON",
                },
                "type": "FOR_LOOP_TEST",
                "expr": [
                    {
                        "type": "BINARY_AFTER_EXPRESSION",
                        "value": "j",
                        "operator": "++",
                        "lineno": 2,
                        "linenoEnd": 2,
                    },
                    {
                        "type": "BINARY_AFTER_EXPRESSION",
                        "value": "i",
                        "operator": "++",
                        "lineno": 2,
                        "linenoEnd": 2,
                    },
                ],
            },
            "type": "FOR_LOOP",
            "lineno": 2,
            "linenoEnd": 4,
            "body": [
                {"type": "INVOCATION", "name": "action", "lineno": 3, "linenoEnd": 3}
            ],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_for_case6(self):

        text = """
        for (int i = 0; ; i++) {
            action();
        }
        """
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "test": {
                "variable": {
                    "type": "ASSIGNMENT",
                    "name": "i",
                    "assign": 0,
                    "operator": "=",
                    "classType": "int",
                    "lineno": 2,
                    "linenoEnd": 2,
                },
                "type": "FOR_LOOP_TEST",
                "expr": {
                    "type": "BINARY_AFTER_EXPRESSION",
                    "value": "i",
                    "operator": "++",
                    "lineno": 2,
                    "linenoEnd": 2,
                },
            },
            "type": "FOR_LOOP",
            "lineno": 2,
            "linenoEnd": 4,
            "body": [
                {"type": "INVOCATION", "name": "action", "lineno": 3, "linenoEnd": 3}
            ],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_for_case7(self):

        text = """
        for (; ; i++) {
            action();
        }
        """
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "test": {
                "type": "FOR_LOOP_TEST",
                "expr": {
                    "type": "BINARY_AFTER_EXPRESSION",
                    "value": "i",
                    "operator": "++",
                    "lineno": 2,
                    "linenoEnd": 2,
                },
            },
            "type": "FOR_LOOP",
            "lineno": 2,
            "linenoEnd": 4,
            "body": [
                {"type": "INVOCATION", "name": "action", "lineno": 3, "linenoEnd": 3}
            ],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_for_case8(self):

        text = """
        for (Something st = get(param); st != null; st = checker.check(param)) {
            action();
        }
        """
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "test": {
                "variable": {
                    "type": "ASSIGNMENT",
                    "name": "st",
                    "assign": {"name": "get", "type": "INVOCATION", "args": ["param"]},
                    "operator": "=",
                    "classType": "Something",
                    "lineno": 2,
                    "linenoEnd": 2,
                },
                "test": {
                    "left": "st",
                    "chain": [{"value": None, "operator": "!="}],
                    "type": "COMPARISON",
                },
                "type": "FOR_LOOP_TEST",
                "expr": {
                    "type": "ASSIGNMENT",
                    "name": "st",
                    "assign": {
                        "name": "checker.check",
                        "type": "INVOCATION",
                        "args": ["param"],
                    },
                    "operator": "=",
                    "lineno": 2,
                    "linenoEnd": 2,
                },
            },
            "type": "FOR_LOOP",
            "lineno": 2,
            "linenoEnd": 4,
            "body": [
                {"type": "INVOCATION", "name": "action", "lineno": 3, "linenoEnd": 3}
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
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "test": "flag",
            "type": "WHILE_LOOP",
            "lineno": 2,
            "linenoEnd": 4,
            "body": [
                {
                    "type": "INVOCATION",
                    "name": "doSomething",
                    "lineno": 3,
                    "linenoEnd": 3,
                }
            ],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_while_case2(self):

        text = """
        while ((int i = getNumber()) > 0) {
            doSomething();
        }
        """
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "test": {
                "left": {
                    "type": "ASSIGNMENT",
                    "name": "i",
                    "assign": {"name": "getNumber", "type": "INVOCATION"},
                    "operator": "=",
                    "classType": "int",
                    "lineno": 2,
                    "linenoEnd": 2,
                },
                "chain": [{"value": 0, "operator": ">"}],
                "type": "COMPARISON",
            },
            "type": "WHILE_LOOP",
            "lineno": 2,
            "linenoEnd": 4,
            "body": [
                {
                    "type": "INVOCATION",
                    "name": "doSomething",
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
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "type": "DO_WHILE_LOOP",
            "lineno": 2,
            "linenoEnd": 4,
            "test": "flag",
            "body": [
                {
                    "type": "INVOCATION",
                    "name": "doSomething",
                    "lineno": 3,
                    "linenoEnd": 3,
                }
            ],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_do_while_case2(self):

        text = """
        do {
            doSomething();
        } while (flag);
        """
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "type": "DO_WHILE_LOOP",
            "lineno": 2,
            "linenoEnd": 4,
            "test": "flag",
            "body": [
                {
                    "type": "INVOCATION",
                    "name": "doSomething",
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
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "type": "TRY",
            "lineno": 2,
            "linenoEnd": 4,
            "body": [
                {
                    "type": "INVOCATION",
                    "name": "doSomething",
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
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "type": "TRY",
            "lineno": 2,
            "linenoEnd": 4,
            "body": [
                {
                    "type": "INVOCATION",
                    "name": "doSomething",
                    "lineno": 3,
                    "linenoEnd": 3,
                }
            ],
            "with": {
                "type": "ASSIGNMENT",
                "name": "r",
                "assign": {"name": "getResource", "type": "INVOCATION"},
                "operator": "=",
                "classType": "Resource",
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
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "type": "TRY",
            "lineno": 2,
            "linenoEnd": 6,
            "catches": [
                {
                    "exceptions": {"name": "ex", "exceptionType": ["Exception"]},
                    "type": "CATCH",
                    "lineno": 4,
                    "linenoEnd": 6,
                    "body": [
                        {
                            "type": "INVOCATION",
                            "name": "doSomethingElse",
                            "lineno": 5,
                            "linenoEnd": 5,
                        }
                    ],
                }
            ],
            "body": [
                {
                    "type": "INVOCATION",
                    "name": "doSomething",
                    "lineno": 3,
                    "linenoEnd": 3,
                }
            ],
            "with": {
                "type": "ASSIGNMENT",
                "name": "r",
                "assign": {"name": "getResource", "type": "INVOCATION"},
                "operator": "=",
                "classType": "Resource",
                "lineno": 2,
                "linenoEnd": 2,
            },
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_try_case4(self):

        text = """
        try (Resource r = getResource()) {
            doSomething();
        } catch (Exception | Error err) {
            doSomethingElse();
        } finally {
            nothing();
        }
        """
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "type": "TRY",
            "lineno": 2,
            "linenoEnd": 8,
            "catches": [
                {
                    "exceptions": {
                        "name": "err",
                        "exceptionType": ["Exception", "Error"],
                    },
                    "type": "CATCH",
                    "lineno": 4,
                    "linenoEnd": 6,
                    "body": [
                        {
                            "type": "INVOCATION",
                            "name": "doSomethingElse",
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
                        "type": "INVOCATION",
                        "name": "nothing",
                        "lineno": 7,
                        "linenoEnd": 7,
                    }
                ],
            },
            "body": [
                {
                    "type": "INVOCATION",
                    "name": "doSomething",
                    "lineno": 3,
                    "linenoEnd": 3,
                }
            ],
            "with": {
                "type": "ASSIGNMENT",
                "name": "r",
                "assign": {"name": "getResource", "type": "INVOCATION"},
                "operator": "=",
                "classType": "Resource",
                "lineno": 2,
                "linenoEnd": 2,
            },
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_try_case5(self):

        text = """
        try (Resource r = getResource()) {
            doSomething();
        } catch (Exception | Error err) {
            doSomethingElse();
        } catch (Exception | Error err2) {
            doSomethingElse();
        } finally {
            no();
        }
        """
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "type": "TRY",
            "lineno": 2,
            "linenoEnd": 10,
            "catches": [
                {
                    "exceptions": {
                        "name": "err",
                        "exceptionType": ["Exception", "Error"],
                    },
                    "type": "CATCH",
                    "lineno": 4,
                    "linenoEnd": 6,
                    "body": [
                        {
                            "type": "INVOCATION",
                            "name": "doSomethingElse",
                            "lineno": 5,
                            "linenoEnd": 5,
                        }
                    ],
                },
                {
                    "exceptions": {
                        "name": "err2",
                        "exceptionType": ["Exception", "Error"],
                    },
                    "type": "CATCH",
                    "lineno": 6,
                    "linenoEnd": 8,
                    "body": [
                        {
                            "type": "INVOCATION",
                            "name": "doSomethingElse",
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
                    {"type": "INVOCATION", "name": "no", "lineno": 9, "linenoEnd": 9}
                ],
            },
            "body": [
                {
                    "type": "INVOCATION",
                    "name": "doSomething",
                    "lineno": 3,
                    "linenoEnd": 3,
                }
            ],
            "with": {
                "type": "ASSIGNMENT",
                "name": "r",
                "assign": {"name": "getResource", "type": "INVOCATION"},
                "operator": "=",
                "classType": "Resource",
                "lineno": 2,
                "linenoEnd": 2,
            },
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_try_case6(self):

        text = """
        try {
            doSomething();
        } catch (Exception | Error err) {
            doSomethingElse();
        } catch (Exception | Error err2) {
            doSomethingElse();
        } finally {
            no();
        }
        """
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "type": "TRY",
            "lineno": 2,
            "linenoEnd": 10,
            "catches": [
                {
                    "exceptions": {
                        "name": "err",
                        "exceptionType": ["Exception", "Error"],
                    },
                    "type": "CATCH",
                    "lineno": 4,
                    "linenoEnd": 6,
                    "body": [
                        {
                            "type": "INVOCATION",
                            "name": "doSomethingElse",
                            "lineno": 5,
                            "linenoEnd": 5,
                        }
                    ],
                },
                {
                    "exceptions": {
                        "name": "err2",
                        "exceptionType": ["Exception", "Error"],
                    },
                    "type": "CATCH",
                    "lineno": 6,
                    "linenoEnd": 8,
                    "body": [
                        {
                            "type": "INVOCATION",
                            "name": "doSomethingElse",
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
                    {"type": "INVOCATION", "name": "no", "lineno": 9, "linenoEnd": 9}
                ],
            },
            "body": [
                {
                    "type": "INVOCATION",
                    "name": "doSomething",
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
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "parameters": ["args"],
            "body": [
                {
                    "type": "INVOCATION",
                    "name": "System.out.println",
                    "args": ['"Let\'s inspect the beans provided by Spring Boot:"'],
                    "lineno": 4,
                    "linenoEnd": 4,
                },
                {
                    "type": "ASSIGNMENT",
                    "name": "beanNames",
                    "assign": {
                        "name": "ctx.getBeanDefinitionNames",
                        "type": "INVOCATION",
                    },
                    "operator": "=",
                    "classType": {"name": "String", "arraySuffix": "[]"},
                    "lineno": 6,
                    "linenoEnd": 6,
                },
                {
                    "type": "INVOCATION",
                    "name": "Arrays.sort",
                    "args": ["beanNames"],
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
                            "type": "INVOCATION",
                            "name": "System.out.println",
                            "args": ["beanName"],
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
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "parameters": ["parameter"],
            "body": [
                {
                    "type": "ARITHMETIC_EXPRESSION",
                    "left": "parameter",
                    "chain": [{"value": '" from lambda"', "operator": "+"}],
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
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "parameters": [{"name": "x", "classType": "int", "type": "PARAMETER"}],
            "body": [
                {
                    "type": "INVOCATION",
                    "name": "System.out.println",
                    "args": [
                        {
                            "left": 2,
                            "chain": [{"value": "x", "operator": "*"}],
                            "type": "ARITHMETIC_EXPRESSION",
                        }
                    ],
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
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "body": [
                {
                    "type": "INVOCATION",
                    "name": "System.out.println",
                    "args": ['"Print somthing!"'],
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
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "name": "list",
            "assign": ["STR_1", "STR_2", "STR_3"],
            "classType": {"name": "String", "arraySuffix": "[]"},
            "operator": "=",
            "type": "ASSIGNMENT",
            "lineno": 1,
            "linenoEnd": 1,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_list_literal_case2(self):

        text = "new String[]{STR_1, STR_2, STR_3};"
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "type": "NEW_EXPRESSION",
            "value": {
                "name": {"name": "String", "arraySuffix": "[]"},
                "type": "ARRAY_LITERAL",
                "value": ["STR_1", "STR_2", "STR_3"],
            },
            "lineno": 1,
            "linenoEnd": 1,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_list_literal_case3(self):

        text = "new String[]{STR_1, STR_2, STR_3,};"
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "type": "NEW_EXPRESSION",
            "value": {
                "name": {"name": "String", "arraySuffix": "[]"},
                "type": "ARRAY_LITERAL",
                "value": ["STR_1", "STR_2", "STR_3"],
            },
            "lineno": 1,
            "linenoEnd": 1,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_list_literal_case4(self):

        text = "String[] arr = {STR_1, STR_2, STR_3,};"
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "type": "ASSIGNMENT",
            "name": "arr",
            "assign": ["STR_1", "STR_2", "STR_3"],
            "operator": "=",
            "classType": {"name": "String", "arraySuffix": "[]"},
            "lineno": 1,
            "linenoEnd": 1,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_special_case1(self):

        text = "name;;"
        tree = get_parser("stmt").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {"body": "name", "type": "STATEMENT", "lineno": 1, "linenoEnd": 1}
        self.assertEqual(result, expected, "Not matched.")
