"""
Method.
"""

from lark import Transformer, v_args


@v_args(meta=True)
class MethodTransformer(Transformer):
    def break_stmt(self, _, meta):
        return {
            "name": "break",
            "type": "BREAK",
            "lineno": meta.line,
            "linenoEnd": meta.end_line,
        }

    def continue_stmt(self, _, meta):
        return {
            "name": "continue",
            "type": "CONTINUE",
            "lineno": meta.line,
            "linenoEnd": meta.end_line,
        }

    def return_stmt(self, child, meta):
        result = {
            "name": "return",
            "type": "RETURN",
            "lineno": meta.line,
            "linenoEnd": meta.end_line,
        }
        if len(child) == 1:
            result["value"] = child[0]
        return result

    def throw_stmt(self, child, meta):
        result = {
            "name": "throw",
            "type": "THROW",
            "lineno": meta.line,
            "linenoEnd": meta.end_line,
        }
        if len(child) == 1:
            result["value"] = child[0]
        return result
