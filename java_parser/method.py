"""
Method.
"""

from lark import Transformer, v_args


@v_args(meta=True)
class MethodTransformer(Transformer):
    def stmt(self, child, _):
        (child,) = child
        return child

    def break_stmt(self, _, meta):
        return {"name": "break", "type": "BREAK"}

    def continue_stmt(self, _, meta):
        return {"name": "continue", "type": "CONTINUE"}

    def return_stmt(self, child, meta):
        result = {"name": "return", "type": "RETURN"}
        if len(child) == 1:
            result["value"] = child[0]
        return result

    def throw_stmt(self, child, meta):
        result = {"name": "throw", "type": "THROW", "value": child[0]}
        return result

    def assign_base(self, child, _):
        if len(child) == 1:
            result = {"name": child[0]}
        else:
            result = {"name": child[0], "assign": child[1]}
        return result

    def assign_type(self, child, _):
        if len(child) == 1:
            result = child[0]
        else:
            result = {**child[1], "classType": child[0]}
        return result

    def assign_modifier(self, child, _):
        if len(child) == 1:
            result = child[0]
        else:
            result = {**child[1], "modifiers": child[0]}
        return result

    def test_stmt(self, child, meta):
        if len(child) == 1:
            result = child[0]
        else:
            result = {**child[1], "comment": child[0]}
        return {
            **result,
            "type": "STATEMENT",
            "lineno": meta.line,
            "linenoEnd": meta.end_line,
        }

    def simple_stmt(self, child, meta):
        if len(child) == 1:
            result = child[0]
        else:
            result = {**child[1], "comment": child[0]}
        return {
            **result,
            "lineno": meta.line,
            "linenoEnd": meta.end_line,
        }

    def small_stmt(self, child, meta):
        (child,) = child
        if type(child) == str:
            child = {"value": child}
        return {**child, "lineno": meta.line, "linenoEnd": meta.end_line}

    def if_stmt(self, child, meta):
        result = {
            "type": "IF",
            "test": child[0],
            "lineno": meta.line,
            "linenoEnd": meta.end_line,
        }
        if len(child) > 1:
            rest = child[1:]
            if type(rest[0]) == list:
                result["value"] = rest[0]
                rest = rest[1:]
            if len(rest) != 0:
                result["chain"] = rest
        return result

    def elif_stmt(self, child, meta):
        result = {
            "type": "ELSE_IF",
            "test": child[0],
            "lineno": meta.line,
            "linenoEnd": meta.end_line,
        }
        if len(child) == 2:
            result["value"] = child[1]
        return result

    def else_stmt(self, child, meta):
        result = {
            "type": "ELSE",
            "lineno": meta.line,
            "linenoEnd": meta.end_line,
        }
        if len(child) == 1:
            result["value"] = child[0]
        return result

    def case_default_suit(self, child, meta):
        if len(child) == 1:
            result = {
                "caseKey": ["<default>"],
                "value": child[0],
                "type": "DEFAULT_CASE",
                "lineno": meta.line,
                "linenoEnd": meta.end_line,
            }
        else:
            result = {
                "caseKey": [*child[0], "<default>"],
                "value": child[1],
                "type": "DEFAULT_CASE",
                "lineno": meta.line,
                "linenoEnd": meta.end_line,
            }
        return result

    def case_key(self, child, meta):
        if len(child) == 1:
            result = child[0]
        else:
            result = "<default>"
        return result

    def case_stmt(self, child, meta):
        result = {
            "caseKey": child[0],
            "value": child[1],
            "type": "CASE",
            "lineno": meta.line,
            "linenoEnd": meta.end_line,
        }
        return result

    def switch_stmt(self, child, meta):
        result = {
            "test": child[0],
            "type": "SWITCH",
            "lineno": meta.line,
            "linenoEnd": meta.end_line,
        }
        if len(child) > 1:
            cases = []
            for x in child[1:]:
                cases = cases + x
            if len(cases) != 0:
                result["cases"] = cases
        return result
