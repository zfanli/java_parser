import unittest
from tests.helper import get_parser
from java_parser.enum import EnumTransformer
from java_parser.field import FieldTransformer
from java_parser.common import CommonTransformer
from java_parser.method import MethodTransformer
from java_parser.annotation import AnnotationTransformer


class CompoundEnumTransformer(
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
        result = CompoundEnumTransformer().transform(tree)
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

    def test_enum_case2(self):

        text = """
        /** Test Enum Type */
        public enum EnumType {
            ENUM_1, ENUM_2, 
            ENUM_3(arg1, arg2),
            /** An enum element with a body */
            ENUM_4(FLAG) {
                @Override
                void someMethod(String name) {
                    doSomething(name);
                }
            }
        }
        """
        tree = get_parser("enum_field").parse(text)
        print(tree)
        result = CompoundEnumTransformer().transform(tree)
        print(result)
        expected = {
            "name": "EnumType",
            "body": [
                {"name": "ENUM_1", "type": "ENUM_ELEMENT", "lineno": 4, "linenoEnd": 4},
                {"name": "ENUM_2", "type": "ENUM_ELEMENT", "lineno": 4, "linenoEnd": 4},
                {
                    "name": "ENUM_3",
                    "args": ["arg1", "arg2"],
                    "type": "ENUM_ELEMENT",
                    "lineno": 5,
                    "linenoEnd": 5,
                },
                {
                    "name": "ENUM_4",
                    "args": ["FLAG"],
                    "body": [
                        {
                            "name": "someMethod",
                            "body": [
                                {
                                    "type": "INVOCATION",
                                    "name": "doSomething",
                                    "args": ["name"],
                                    "lineno": 10,
                                    "linenoEnd": 10,
                                }
                            ],
                            "parameters": [
                                {
                                    "name": "name",
                                    "classType": "String",
                                    "type": "PARAMETER",
                                }
                            ],
                            "returnType": "void",
                            "type": "METHOD",
                            "annotations": [
                                {
                                    "name": "Override",
                                    "lineno": 8,
                                    "linenoEnd": 8,
                                    "type": "ANNOTATION",
                                }
                            ],
                            "lineno": 8,
                            "linenoEnd": 11,
                        }
                    ],
                    "comment": ["/** An enum element with a body */"],
                    "type": "ENUM_ELEMENT",
                    "lineno": 6,
                    "linenoEnd": 12,
                },
            ],
            "modifiers": ["public"],
            "comment": ["/** Test Enum Type */"],
            "type": "ENUM_FIELD",
            "lineno": 2,
            "linenoEnd": 13,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_enum_case3(self):

        text = """
            ENUM_1, ENUM_2, 
            ENUM_3(arg1, arg2),
            /** An enum element with a body */
            ENUM_4(FLAG) {
                @Override
                void someMethod(String name) {
                    doSomething(name);
                }
            };
        """
        tree = get_parser("enum_class_elem").parse(text)
        print(tree)
        result = CompoundEnumTransformer().transform(tree)
        print(result)
        expected = {
            "body": [
                [
                    {
                        "name": "ENUM_1",
                        "type": "ENUM_ELEMENT",
                        "lineno": 2,
                        "linenoEnd": 2,
                    },
                    {
                        "name": "ENUM_2",
                        "type": "ENUM_ELEMENT",
                        "lineno": 2,
                        "linenoEnd": 2,
                    },
                    {
                        "name": "ENUM_3",
                        "args": ["arg1", "arg2"],
                        "type": "ENUM_ELEMENT",
                        "lineno": 3,
                        "linenoEnd": 3,
                    },
                    {
                        "name": "ENUM_4",
                        "args": ["FLAG"],
                        "body": [
                            {
                                "name": "someMethod",
                                "body": [
                                    {
                                        "type": "INVOCATION",
                                        "name": "doSomething",
                                        "args": ["name"],
                                        "lineno": 8,
                                        "linenoEnd": 8,
                                    }
                                ],
                                "parameters": [
                                    {
                                        "name": "name",
                                        "classType": "String",
                                        "type": "PARAMETER",
                                    }
                                ],
                                "returnType": "void",
                                "type": "METHOD",
                                "annotations": [
                                    {
                                        "name": "Override",
                                        "lineno": 6,
                                        "linenoEnd": 6,
                                        "type": "ANNOTATION",
                                    }
                                ],
                                "lineno": 6,
                                "linenoEnd": 9,
                            }
                        ],
                        "comment": ["/** An enum element with a body */"],
                        "type": "ENUM_ELEMENT",
                        "lineno": 4,
                        "linenoEnd": 10,
                    },
                ]
            ],
            "type": "ENUM_ELEMENTS",
            "lineno": 2,
            "linenoEnd": 10,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_enum_case3(self):

        text = """
            ENUM_1, ENUM_2, ENUM_3,;
        """
        tree = get_parser("enum_class_elem").parse(text)
        print(tree)
        result = CompoundEnumTransformer().transform(tree)
        print(result)
        expected = {
            "body": [
                [
                    {
                        "name": "ENUM_1",
                        "type": "ENUM_ELEMENT",
                        "lineno": 2,
                        "linenoEnd": 2,
                    },
                    {
                        "name": "ENUM_2",
                        "type": "ENUM_ELEMENT",
                        "lineno": 2,
                        "linenoEnd": 2,
                    },
                    {
                        "name": "ENUM_3",
                        "type": "ENUM_ELEMENT",
                        "lineno": 2,
                        "linenoEnd": 2,
                    },
                ]
            ],
            "type": "ENUM_ELEMENTS",
            "lineno": 2,
            "linenoEnd": 2,
        }
        self.assertEqual(result, expected, "Not matched.")

