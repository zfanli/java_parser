"""
Package.
"""

from lark import Transformer, v_args


@v_args(meta=True)
class ImportTransformer(Transformer):
    def import_stmt(self, child, meta):

        if len(child) == 1:
            (child,) = child
            modifier = None
        else:
            (modifier, child) = child

        result = {
            "import": child,
            "type": "IMPORT",
            "lineno": meta.line,
            "linenoEnd": meta.end_line,
        }

        if modifier:
            result["modifier"] = modifier

        return result

    def imports(self, child, _):
        return child
