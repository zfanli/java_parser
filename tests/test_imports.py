import unittest
from tests.helper import get_parser
from java_parser.imports import ImportTransformer
from java_parser.common import CommonTransformer


class CompoundImportTransformer(CommonTransformer, ImportTransformer):
    pass


class TestImport(unittest.TestCase):
    def test_import_case1(self):

        text = "import path.to.package.ClassName;"
        tree = get_parser("import_stmt").parse(text)
        print(tree)
        result = CompoundImportTransformer().transform(tree)
        print(result)
        expected = {
            "value": "path.to.package.ClassName",
            "type": "IMPORT",
            "lineno": 1,
            "linenoEnd": 1,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_import_case2(self):

        text = "import path.to.package.*;"
        tree = get_parser("import_stmt").parse(text)
        print(tree)
        result = CompoundImportTransformer().transform(tree)
        print(result)
        expected = {
            "value": "path.to.package.*",
            "type": "IMPORT",
            "lineno": 1,
            "linenoEnd": 1,
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_import_case3(self):

        text = "import static path.to.package.*;"
        tree = get_parser("import_stmt").parse(text)
        print(tree)
        result = CompoundImportTransformer().transform(tree)
        print(result)
        expected = {
            "value": "path.to.package.*",
            "type": "IMPORT",
            "lineno": 1,
            "linenoEnd": 1,
            "modifier": "static",
        }
        self.assertEqual(result, expected, "Not matched.")

    def test_import_case4(self):

        text = """
        import static path.to.package.*;
        import java.util.ArrayList;
        import some.other.package.ClassName;
        """
        tree = get_parser("imports").parse(text)
        print(tree)
        result = CompoundImportTransformer().transform(tree)
        print(result)
        expected = [
            {
                "value": "path.to.package.*",
                "type": "IMPORT",
                "lineno": 2,
                "linenoEnd": 2,
                "modifier": "static",
            },
            {
                "value": "java.util.ArrayList",
                "type": "IMPORT",
                "lineno": 3,
                "linenoEnd": 3,
            },
            {
                "value": "some.other.package.ClassName",
                "type": "IMPORT",
                "lineno": 4,
                "linenoEnd": 4,
            },
        ]
        self.assertEqual(result, expected, "Not matched.")
