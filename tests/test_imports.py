import unittest
from tests.helper import get_parser
from java_parser.imports import ImportTransformer
from java_parser.common import CommonTransformer


class TestImportTransformer(CommonTransformer, ImportTransformer):
    pass


class TestPackage(unittest.TestCase):
    def test_package_case1(self):

        text = "import path.to.package.ClassName;"
        tree = get_parser("import_stmt").parse(text)
        print(tree)
        result = TestImportTransformer().transform(tree)
        print(result)
        expected = {"import": "path.to.package.ClassName", "lineno": 1, "linenoEnd": 1}
        self.assertEqual(result, expected, "Not matched.")

    def test_package_case2(self):

        text = "import path.to.package.*;"
        tree = get_parser("import_stmt").parse(text)
        print(tree)
        result = TestImportTransformer().transform(tree)
        print(result)
        expected = {"import": "path.to.package.*", "lineno": 1, "linenoEnd": 1}
        self.assertEqual(result, expected, "Not matched.")
