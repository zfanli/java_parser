import unittest
from tests.helper import get_parser
from java_parser.package import PackageTransformer
from java_parser.common import CommonTransformer


class CompoundPackageTransformer(CommonTransformer, PackageTransformer):
    pass


class TestPackage(unittest.TestCase):
    def test_package_case1(self):

        text = "package path.to.package.PackageName;"
        tree = get_parser("package_stmt").parse(text)
        print(tree)
        result = CompoundPackageTransformer().transform(tree)
        print(result)
        expected = {
            "value": "path.to.package.PackageName",
            "type": "PACKAGE",
            "lineno": 1,
            "linenoEnd": 1,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_package_case2(self):

        text = "package path.to.package.*;"
        tree = get_parser("package_stmt").parse(text)
        print(tree)
        result = CompoundPackageTransformer().transform(tree)
        print(result)
        expected = {
            "value": "path.to.package.*",
            "type": "PACKAGE",
            "lineno": 1,
            "linenoEnd": 1,
        }
        self.assertEqual(result, expected, "Not matched.")
