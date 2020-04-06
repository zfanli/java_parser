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
        expected = {"annotation": "AnnotationTest", "lineno": 1, "linenoEnd": 1}
        self.assertEqual(result, expected, "Not matched.")
