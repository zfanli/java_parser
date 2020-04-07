import unittest
from tests.helper import get_parser
from java_parser.annotation import AnnotationTransformer
from java_parser.common import CommonTransformer


class TestAnnotationTransformer(CommonTransformer, AnnotationTransformer):
    pass


class TestAnnotation(unittest.TestCase):
    def test_annotation_case1(self):

        text = "@AnnotationTest"
        tree = get_parser("annotation").parse(text)
        print(tree)
        result = TestAnnotationTransformer().transform(tree)
        print(result)
        expected = {
            "value": "AnnotationTest",
            "lineno": 1,
            "linenoEnd": 1,
            "type": "ANNOTATION",
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_annotation_case2(self):

        text = "@AnnotationTest()"
        tree = get_parser("annotation").parse(text)
        print(tree)
        result = TestAnnotationTransformer().transform(tree)
        print(result)
        expected = {
            "value": "AnnotationTest",
            "lineno": 1,
            "linenoEnd": 1,
            "type": "ANNOTATION",
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_annotation_case3(self):

        text = '@AnnotationTest("Literal")'
        tree = get_parser("annotation").parse(text)
        print(tree)
        result = TestAnnotationTransformer().transform(tree)
        print(result)
        expected = {
            "value": "AnnotationTest",
            "lineno": 1,
            "linenoEnd": 1,
            "type": "ANNOTATION",
            "param": ['"Literal"'],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_annotation_case4(self):

        text = '@AnnotationTest("Literal", true, -1, Name)'
        tree = get_parser("annotation").parse(text)
        print(tree)
        result = TestAnnotationTransformer().transform(tree)
        print(result)
        expected = {
            "value": "AnnotationTest",
            "lineno": 1,
            "linenoEnd": 1,
            "type": "ANNOTATION",
            "param": ['"Literal"', True, -1.0, "Name"],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_annotation_case5(self):

        text = "@AnnotationTest({ test })"
        tree = get_parser("annotation").parse(text)
        print(tree)
        result = TestAnnotationTransformer().transform(tree)
        print(result)
        expected = {
            "value": "AnnotationTest",
            "lineno": 1,
            "linenoEnd": 1,
            "type": "ANNOTATION",
            "param": [{"key": "<default>", "value": ["test"]}],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_annotation_case6(self):

        text = '@AnnotationTest({ test, "Literal", false, 123 })'
        tree = get_parser("annotation").parse(text)
        print(tree)
        result = TestAnnotationTransformer().transform(tree)
        print(result)
        expected = {
            "value": "AnnotationTest",
            "lineno": 1,
            "linenoEnd": 1,
            "type": "ANNOTATION",
            "param": [
                {"key": "<default>", "value": ["test", '"Literal"', False, 123.0]}
            ],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_annotation_case7(self):

        text = '@AnnotationTest(key1="test", key2=true, key3=Attribute)'
        tree = get_parser("annotation").parse(text)
        print(tree)
        result = TestAnnotationTransformer().transform(tree)
        print(result)
        expected = {
            "value": "AnnotationTest",
            "lineno": 1,
            "linenoEnd": 1,
            "type": "ANNOTATION",
            "param": [
                {"key": "key1", "value": '"test"'},
                {"key": "key2", "value": True},
                {"key": "key3", "value": "Attribute"},
            ],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_annotation_case8(self):

        text = "@AnnotationTest(key1= @Filter(something))"
        tree = get_parser("annotation").parse(text)
        print(tree)
        result = TestAnnotationTransformer().transform(tree)
        print(result)
        expected = {
            "value": "AnnotationTest",
            "lineno": 1,
            "linenoEnd": 1,
            "type": "ANNOTATION",
            "param": [
                {
                    "key": "key1",
                    "value": {
                        "value": "Filter",
                        "lineno": 1,
                        "linenoEnd": 1,
                        "type": "ANNOTATION",
                        "param": ["something"],
                    },
                }
            ],
        }
        self.assertEqual(result, expected, "Not matched.")
