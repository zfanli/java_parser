import unittest
from tests.helper import get_parser
from java_parser.method import MethodTransformer
from java_parser.annotation import AnnotationTransformer
from java_parser.common import CommonTransformer


class CompoundMethodTransformer(
    CommonTransformer, AnnotationTransformer, MethodTransformer
):
    pass


class TestMethod(unittest.TestCase):
    def test_method_case1(self):

        text = """
        public static void main(String[] args) {
            SpringApplication.run(Application.class, args);
        }
        """
        tree = get_parser("method").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "name": "main",
            "body": [
                {
                    "body": {
                        "name": "SpringApplication.run",
                        "type": "INVOCATION",
                        "args": ["Application.class", "args"],
                    },
                    "type": "STATEMENT",
                    "lineno": 3,
                    "linenoEnd": 3,
                }
            ],
            "parameters": [
                {
                    "name": "args",
                    "classType": {"name": "String", "arraySuffix": "[]"},
                    "type": "PARAMETER",
                }
            ],
            "returnType": "void",
            "type": "METHOD",
            "modifiers": ["public", "static"],
            "lineno": 2,
            "linenoEnd": 4,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_method_case2(self):

        text = """
        /**
        * Some comments.
        * 
        * @param param other things...
        */
        @Annotation("something here")
        public static void main(String[] args) {
            SpringApplication.run(Application.class, args);
        }
        """
        tree = get_parser("method").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "name": "main",
            "body": [
                {
                    "body": {
                        "name": "SpringApplication.run",
                        "type": "INVOCATION",
                        "args": ["Application.class", "args"],
                    },
                    "type": "STATEMENT",
                    "lineno": 9,
                    "linenoEnd": 9,
                }
            ],
            "parameters": [
                {
                    "name": "args",
                    "classType": {"name": "String", "arraySuffix": "[]"},
                    "type": "PARAMETER",
                }
            ],
            "returnType": "void",
            "type": "METHOD",
            "modifiers": ["public", "static"],
            "annotations": [
                {
                    "name": "Annotation",
                    "lineno": 7,
                    "linenoEnd": 7,
                    "type": "ANNOTATION",
                    "param": ['"something here"'],
                }
            ],
            "comment": [
                "/**",
                "* Some comments.",
                "* ",
                "* @param param other things...",
                "*/",
            ],
            "lineno": 2,
            "linenoEnd": 10,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_method_case3(self):

        text = """
        /**
        * This is a constructor.
        */
        @Starter(Debug=true)
        public ThisConstructor() throws Exception, Error {
            SpringApplication.run(Application.class, args);
        }
        """
        tree = get_parser("method").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "name": "ThisConstructor",
            "body": [
                {
                    "body": {
                        "name": "SpringApplication.run",
                        "type": "INVOCATION",
                        "args": ["Application.class", "args"],
                    },
                    "type": "STATEMENT",
                    "lineno": 7,
                    "linenoEnd": 7,
                }
            ],
            "throws": ["Exception", "Error"],
            "type": "CONSTRUCTOR",
            "modifiers": ["public"],
            "annotations": [
                {
                    "name": "Starter",
                    "lineno": 5,
                    "linenoEnd": 5,
                    "type": "ANNOTATION",
                    "param": [{"key": "Debug", "value": True}],
                }
            ],
            "comment": ["/**", "* This is a constructor.", "*/"],
            "lineno": 2,
            "linenoEnd": 8,
        }
        self.assertEqual(result, expected, "Not matched.")
