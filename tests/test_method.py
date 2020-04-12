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
                    "type": "INVOCATION",
                    "name": "SpringApplication.run",
                    "args": ["Application.class", "args"],
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
                    "type": "INVOCATION",
                    "name": "SpringApplication.run",
                    "args": ["Application.class", "args"],
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
                    "args": ['"something here"'],
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
            "throws": ["Exception", "Error"],
            "body": [
                {
                    "type": "INVOCATION",
                    "name": "SpringApplication.run",
                    "args": ["Application.class", "args"],
                    "lineno": 7,
                    "linenoEnd": 7,
                }
            ],
            "type": "CONSTRUCTOR",
            "modifiers": ["public"],
            "annotations": [
                {
                    "name": "Starter",
                    "lineno": 5,
                    "linenoEnd": 5,
                    "type": "ANNOTATION",
                    "args": [{"key": "Debug", "value": True}],
                }
            ],
            "comment": ["/**", "* This is a constructor.", "*/"],
            "lineno": 2,
            "linenoEnd": 8,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_method_case4(self):

        text = """
        /**
        * This is a constructor.
        */
        public ThisConstructor() throws Exception, Error;
        """
        tree = get_parser("method").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "name": "ThisConstructor",
            "throws": ["Exception", "Error"],
            "type": "CONSTRUCTOR",
            "modifiers": ["public"],
            "comment": ["/**", "* This is a constructor.", "*/"],
            "lineno": 2,
            "linenoEnd": 5,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_method_case5(self):
        text = """
        protected abstract ReturnClassType AbstractMethodName();
        """
        tree = get_parser("method").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "name": "AbstractMethodName",
            "returnType": "ReturnClassType",
            "type": "METHOD",
            "modifiers": ["protected", "abstract"],
            "lineno": 2,
            "linenoEnd": 2,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_block_case1(self):

        text = """
        static {
            doSomething();
        }
        """
        tree = get_parser("block").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "body": [
                {
                    "type": "INVOCATION",
                    "name": "doSomething",
                    "lineno": 3,
                    "linenoEnd": 3,
                }
            ],
            "modifiers": ["static"],
            "type": "STATIC_BLOCK",
            "lineno": 2,
            "linenoEnd": 4,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_block_case2(self):

        text = """
        {
            doSomething();
        }
        """
        tree = get_parser("block").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "body": [
                {
                    "type": "INVOCATION",
                    "name": "doSomething",
                    "lineno": 3,
                    "linenoEnd": 3,
                }
            ],
            "type": "BLOCK",
            "lineno": 2,
            "linenoEnd": 4,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_parameter_case1(self):

        text = """
        String name
        """
        tree = get_parser("parameter").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {"name": "name", "classType": "String", "type": "PARAMETER"}
        self.assertEqual(result, expected, "Not matched.")

    def test_parameter_case2(self):

        text = """
        @FieldAnnotation String name
        """
        tree = get_parser("parameter").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "name": "name",
            "classType": "String",
            "annotations": [
                {
                    "name": "FieldAnnotation",
                    "lineno": 2,
                    "linenoEnd": 2,
                    "type": "ANNOTATION",
                }
            ],
            "type": "PARAMETER",
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_parameter_case3(self):

        text = """
        String... args
        """
        tree = get_parser("parameter").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {"name": "args", "classType": "String...", "type": "PARAMETER"}
        self.assertEqual(result, expected, "Not matched.")

    def test_parameter_case4(self):

        text = """
        Class<?> anyClass
        """
        tree = get_parser("parameter").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "name": "anyClass",
            "classType": {"name": "Class", "generic": ["?"]},
            "type": "PARAMETER",
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_parameter_case5(self):

        text = """
        String name, int age, Info info, String[] other
        """
        tree = get_parser("parameters").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = [
            {"name": "name", "classType": "String", "type": "PARAMETER"},
            {"name": "age", "classType": "int", "type": "PARAMETER"},
            {"name": "info", "classType": "Info", "type": "PARAMETER"},
            {
                "name": "other",
                "classType": {"name": "String", "arraySuffix": "[]"},
                "type": "PARAMETER",
            },
        ]
        self.assertEqual(result, expected, "Not matched.")

    def test_parameter_case6(self):

        text = """
        @Input InputType in
        """
        tree = get_parser("parameter").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {
            "name": "in",
            "classType": "InputType",
            "annotations": [
                {"name": "Input", "lineno": 2, "linenoEnd": 2, "type": "ANNOTATION"}
            ],
            "type": "PARAMETER",
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_return_type_case1(self):

        text = """
        <T> T
        """
        tree = get_parser("return_type").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {"generic": ["T"], "name": "T"}
        self.assertEqual(result, expected, "Not matched.")

    def test_return_type_case2(self):

        text = """
        <T> List<T>
        """
        tree = get_parser("return_type").parse(text)
        print(tree)
        result = CompoundMethodTransformer().transform(tree)
        print(result)
        expected = {"generic": ["T"], "name": {"name": "List", "generic": ["T"]}}
        self.assertEqual(result, expected, "Not matched.")
