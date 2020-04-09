"""
Package.
"""

from lark import Transformer, v_args


@v_args(meta=True)
class PackageTransformer(Transformer):
    def package_stmt(self, child, meta):

        (child,) = child

        return {
            "value": child,
            "type": "PACKAGE",
            "lineno": meta.line,
            "linenoEnd": meta.end_line,
        }
