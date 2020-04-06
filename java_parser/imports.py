"""
Package.
"""

from lark import Transformer, v_args


@v_args(meta=True)
class ImportTransformer(Transformer):
    def import_stmt(self, child, meta):

        (child,) = child

        return {
            "import": child,
            "lineno": meta.line,
            "linenoEnd": meta.end_line,
        }
