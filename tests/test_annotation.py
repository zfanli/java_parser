import unittest
from tests.helper import get_parser
from java_parser.annotation import AnnotationTransformer
from java_parser.common import CommonTransformer


class CompoundAnnotationTransformer(CommonTransformer, AnnotationTransformer):
    pass


class TestAnnotation(unittest.TestCase):
    def test_annotation_case1(self):

        text = "@AnnotationTest"
        tree = get_parser("annotation").parse(text)
        print(tree)
        result = CompoundAnnotationTransformer().transform(tree)
        print(result)
        expected = {
            "name": "AnnotationTest",
            "lineno": 1,
            "linenoEnd": 1,
            "type": "ANNOTATION",
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_annotation_case2(self):

        text = "@AnnotationTest()"
        tree = get_parser("annotation").parse(text)
        print(tree)
        result = CompoundAnnotationTransformer().transform(tree)
        print(result)
        expected = {
            "name": "AnnotationTest",
            "lineno": 1,
            "linenoEnd": 1,
            "type": "ANNOTATION",
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_annotation_case3(self):

        text = '@AnnotationTest("Literal")'
        tree = get_parser("annotation").parse(text)
        print(tree)
        result = CompoundAnnotationTransformer().transform(tree)
        print(result)
        expected = {
            "name": "AnnotationTest",
            "lineno": 1,
            "linenoEnd": 1,
            "type": "ANNOTATION",
            "args": ['"Literal"'],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_annotation_case4(self):

        text = '@AnnotationTest("Literal", true, -1, Name)'
        tree = get_parser("annotation").parse(text)
        print(tree)
        result = CompoundAnnotationTransformer().transform(tree)
        print(result)
        expected = {
            "name": "AnnotationTest",
            "lineno": 1,
            "linenoEnd": 1,
            "type": "ANNOTATION",
            "args": ['"Literal"', True, -1.0, "Name"],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_annotation_case5(self):

        text = "@AnnotationTest({ test })"
        tree = get_parser("annotation").parse(text)
        print(tree)
        result = CompoundAnnotationTransformer().transform(tree)
        print(result)
        expected = {
            "name": "AnnotationTest",
            "lineno": 1,
            "linenoEnd": 1,
            "type": "ANNOTATION",
            "args": [{"value": ["test"]}],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_annotation_case6(self):

        text = '@AnnotationTest({ test, "Literal", false, 123 })'
        tree = get_parser("annotation").parse(text)
        print(tree)
        result = CompoundAnnotationTransformer().transform(tree)
        print(result)
        expected = {
            "name": "AnnotationTest",
            "lineno": 1,
            "linenoEnd": 1,
            "type": "ANNOTATION",
            "args": [{"value": ["test", '"Literal"', False, 123.0]}],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_annotation_case7(self):

        text = '@AnnotationTest(key1="test", key2=true, key3=Attribute)'
        tree = get_parser("annotation").parse(text)
        print(tree)
        result = CompoundAnnotationTransformer().transform(tree)
        print(result)
        expected = {
            "name": "AnnotationTest",
            "lineno": 1,
            "linenoEnd": 1,
            "type": "ANNOTATION",
            "args": [
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
        result = CompoundAnnotationTransformer().transform(tree)
        print(result)
        expected = {
            "name": "AnnotationTest",
            "lineno": 1,
            "linenoEnd": 1,
            "type": "ANNOTATION",
            "args": [
                {
                    "key": "key1",
                    "value": {
                        "name": "Filter",
                        "lineno": 1,
                        "linenoEnd": 1,
                        "type": "ANNOTATION",
                        "args": ["something"],
                    },
                }
            ],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_annotation_case9(self):

        text = '@Annotation(Key={"val1", "val2"}, Other=Parameter.another)'
        tree = get_parser("annotation").parse(text)
        print(tree)
        result = CompoundAnnotationTransformer().transform(tree)
        print(result)
        expected = {
            "name": "Annotation",
            "lineno": 1,
            "linenoEnd": 1,
            "type": "ANNOTATION",
            "args": [
                {"key": "Key", "value": ['"val1"', '"val2"']},
                {"key": "Other", "value": "Parameter.another"},
            ],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_annotation_case10(self):

        text = '@Annotation("/PATH")'
        tree = get_parser("annotation").parse(text)
        print(tree)
        result = CompoundAnnotationTransformer().transform(tree)
        print(result)
        expected = {
            "name": "Annotation",
            "lineno": 1,
            "linenoEnd": 1,
            "type": "ANNOTATION",
            "args": ['"/PATH"'],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_annotation_case11(self):

        text = "@Import({Target.class })"
        tree = get_parser("annotation").parse(text)
        print(tree)
        result = CompoundAnnotationTransformer().transform(tree)
        print(result)
        expected = {
            "name": "Import",
            "lineno": 1,
            "linenoEnd": 1,
            "type": "ANNOTATION",
            "args": [{"value": ["Target.class"]}],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_annotation_case12(self):

        text = """@ComponentScan(
            includeFilters = @Filter(
                type = FilterType.REGEX, 
                pattern = ".*pattern"
            ), 
            basePackages = "package", 
            useDefaultFilters = false
        )
        """
        tree = get_parser("annotation").parse(text)
        print(tree)
        result = CompoundAnnotationTransformer().transform(tree)
        print(result)
        expected = {
            "name": "ComponentScan",
            "lineno": 1,
            "linenoEnd": 8,
            "type": "ANNOTATION",
            "args": [
                {
                    "key": "includeFilters",
                    "value": {
                        "name": "Filter",
                        "lineno": 2,
                        "linenoEnd": 5,
                        "type": "ANNOTATION",
                        "args": [
                            {"key": "type", "value": "FilterType.REGEX"},
                            {"key": "pattern", "value": '".*pattern"'},
                        ],
                    },
                },
                {"key": "basePackages", "value": '"package"'},
                {"key": "useDefaultFilters", "value": False},
            ],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_annotation_case13(self):

        text = """
        @Test
        @Annotation(Value)
        @MultiValues(value={Value1, value2})
        @ListValues(Value1, Value2)
        """
        tree = get_parser("annotations").parse(text)
        print(tree)
        result = CompoundAnnotationTransformer().transform(tree)
        print(result)
        expected = [
            {"name": "Test", "lineno": 2, "linenoEnd": 2, "type": "ANNOTATION"},
            {
                "name": "Annotation",
                "lineno": 3,
                "linenoEnd": 3,
                "type": "ANNOTATION",
                "args": ["Value"],
            },
            {
                "name": "MultiValues",
                "lineno": 4,
                "linenoEnd": 4,
                "type": "ANNOTATION",
                "args": [{"key": "value", "value": ["Value1", "value2"]}],
            },
            {
                "name": "ListValues",
                "lineno": 5,
                "linenoEnd": 5,
                "type": "ANNOTATION",
                "args": ["Value1", "Value2"],
            },
        ]
        self.assertEqual(result, expected, "Not matched.")

    def test_annotation_case14(self):

        text = """
        @Literal1("string")
        @Literal2("string", "another")
        @Literal3(123)
        @Literal4(123, 456)
        @Literal5(1.1)
        @Literal6(1.1, 9.9)
        @Literal7(true)
        @Literal8(false, true)
        """
        tree = get_parser("annotations").parse(text)
        print(tree)
        result = CompoundAnnotationTransformer().transform(tree)
        print(result)
        expected = [
            {
                "name": "Literal1",
                "lineno": 2,
                "linenoEnd": 2,
                "type": "ANNOTATION",
                "args": ['"string"'],
            },
            {
                "name": "Literal2",
                "lineno": 3,
                "linenoEnd": 3,
                "type": "ANNOTATION",
                "args": ['"string"', '"another"'],
            },
            {
                "name": "Literal3",
                "lineno": 4,
                "linenoEnd": 4,
                "type": "ANNOTATION",
                "args": [123.0],
            },
            {
                "name": "Literal4",
                "lineno": 5,
                "linenoEnd": 5,
                "type": "ANNOTATION",
                "args": [123.0, 456.0],
            },
            {
                "name": "Literal5",
                "lineno": 6,
                "linenoEnd": 6,
                "type": "ANNOTATION",
                "args": [1.1],
            },
            {
                "name": "Literal6",
                "lineno": 7,
                "linenoEnd": 7,
                "type": "ANNOTATION",
                "args": [1.1, 9.9],
            },
            {
                "name": "Literal7",
                "lineno": 8,
                "linenoEnd": 8,
                "type": "ANNOTATION",
                "args": [True],
            },
            {
                "name": "Literal8",
                "lineno": 9,
                "linenoEnd": 9,
                "type": "ANNOTATION",
                "args": [False, True],
            },
        ]
        self.assertEqual(result, expected, "Not matched.")

    def test_annotation_case15(self):

        text = """
        @EmptyList(@Another(ok))
        """
        tree = get_parser("annotation").parse(text)
        print(tree)
        result = CompoundAnnotationTransformer().transform(tree)
        print(result)
        expected = {
            "name": "EmptyList",
            "lineno": 2,
            "linenoEnd": 2,
            "type": "ANNOTATION",
            "args": [
                {
                    "name": "Another",
                    "lineno": 2,
                    "linenoEnd": 2,
                    "type": "ANNOTATION",
                    "args": ["ok"],
                }
            ],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_annotation_case16(self):

        text = """
        @EmptyList({})
        """
        tree = get_parser("annotation").parse(text)
        print(tree)
        result = CompoundAnnotationTransformer().transform(tree)
        print(result)
        expected = {
            "name": "EmptyList",
            "lineno": 2,
            "linenoEnd": 2,
            "type": "ANNOTATION",
            "args": ["{}"],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_annotation_case17(self):

        text = """
        @RunWith(SpringRunner.class)
        """
        tree = get_parser("annotation").parse(text)
        print(tree)
        result = CompoundAnnotationTransformer().transform(tree)
        print(result)
        expected = {
            "name": "RunWith",
            "lineno": 2,
            "linenoEnd": 2,
            "type": "ANNOTATION",
            "args": ["SpringRunner.class"],
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_annotation_case18(self):

        text = """
        @Annotation(key = "Test" + "String")
        """
        tree = get_parser("annotation").parse(text)
        print(tree)
        result = CompoundAnnotationTransformer().transform(tree)
        print(result)
        expected = {
            "name": "Annotation",
            "lineno": 2,
            "linenoEnd": 2,
            "type": "ANNOTATION",
            "args": [
                {
                    "key": "key",
                    "left": '"Test"',
                    "chain": [{"value": '"String"', "operator": "+"}],
                    "type": "ARITHMETIC_EXPRESSION",
                }
            ],
        }
        self.assertEqual(result, expected, "Not matched.")

