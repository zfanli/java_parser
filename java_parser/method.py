"""
Method.
"""

from lark import Transformer, v_args


@v_args(meta=True)
class MethodTransformer(Transformer):
    def stmt(self, child, meta):
        if len(child) == 1:
            result = child[0]
        else:
            result = {**child[1], "comment": child[0]}
        return {
            **result,
            "lineno": meta.line,
            "linenoEnd": meta.end_line,
        }

    def break_stmt(self, _, meta):
        return {"body": "break", "type": "BREAK"}

    def continue_stmt(self, _, meta):
        return {"body": "continue", "type": "CONTINUE"}

    def return_stmt(self, child, meta):
        result = {"body": "return", "type": "RETURN"}
        if len(child) == 1:
            result["body"] = child[0]
        return result

    def throw_stmt(self, child, meta):
        result = {"type": "THROW", "body": child[0]}
        return result

    def assert_stmt(self, child, meta):
        result = {"type": "ASSERT", "body": child[0]}
        return result

    def assign_base(self, child, _):
        if len(child) == 1:
            result = {"body": child[0]}
        else:
            result = {
                "name": child[0],
                "assign": child[2],
                "operator": str(child[1]),
                "type": "ASSIGNMENT",
            }
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

    def arr_operation(self, child, _):
        return {"name": child[0], "index": child[1], "type": "ARRAY_OPERATION"}

    def test_stmt(self, child, meta):
        return {
            "type": "STATEMENT",
            **child[0],
            "lineno": meta.line,
            "linenoEnd": meta.end_line,
        }

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
                result["body"] = rest[0]
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
            result["body"] = child[1]
        return result

    def else_stmt(self, child, meta):
        result = {
            "type": "ELSE",
            "lineno": meta.line,
            "linenoEnd": meta.end_line,
        }
        if len(child) == 1:
            result["body"] = child[0]
        return result

    def case_key(self, child, meta):
        if len(child) == 1:
            result = {"caseKey": child[0]}
        else:
            result = {"caseKey": "default"}
        return result

    def case_suit(self, child, meta):
        result = {
            **child[0],
            "type": "CASE",
            "lineno": meta.line,
            "linenoEnd": meta.end_line,
        }
        if len(child) == 2:
            result["body"] = child[1]
        return result

    def switch_stmt(self, child, meta):
        result = {
            "test": child[0],
            "type": "SWITCH",
            "lineno": meta.line,
            "linenoEnd": meta.end_line,
        }
        if len(child) == 2 and len(child[1]) > 0:
            result["cases"] = child[1]
        return result

    def for_loop_test(self, child, _):
        result = {
            "variable": child[0],
            "test": child[1],
            "type": "FOR_LOOP_TEST",
        }
        if len(child) == 3:
            result["expr"] = child[2]
        return result

    def for_each_test(self, child, _):
        return {
            "variable": child[1],
            "classType": child[0],
            "list": child[2],
            "type": "FOR_EACH_TEST",
        }

    def for_stmt(self, child, meta):
        result = {
            "test": child[0],
            "type": "FOR_LOOP",
            "lineno": meta.line,
            "linenoEnd": meta.end_line,
        }
        if len(child) == 2:
            result["body"] = child[1]
        return result

    def while_stmt(self, child, meta):
        result = {
            "test": child[0],
            "type": "WHILE_LOOP",
            "lineno": meta.line,
            "linenoEnd": meta.end_line,
        }
        if len(child) == 2:
            result["body"] = child[1]
        return result

    def do_while_stmt(self, child, meta):
        result = {
            "type": "DO_WHILE_LOOP",
            "lineno": meta.line,
            "linenoEnd": meta.end_line,
        }
        if len(child) == 1:
            result["test"] = child[0]
        else:
            result["test"] = child[1]
            result["body"] = child[0]
        return result

    def finally_stmt(self, child, meta):
        result = {
            "type": "FINALLY",
            "lineno": meta.line,
            "linenoEnd": meta.end_line,
        }
        if len(child) == 1:
            result["body"] = child[0]
        return result

    def catch_stmt(self, child, meta):
        result = {
            "exceptions": child[0],
            "type": "CATCH",
            "lineno": meta.line,
            "linenoEnd": meta.end_line,
        }
        if len(child) == 2:
            result["body"] = child[1]
        return result

    def catch_finally_stmt(self, child, meta):
        result = {}
        for x in child:
            if type(x) == dict:
                result["finally"] = x
            else:
                if len(x) > 0:
                    result["catches"] = x
        return result

    def try_body(self, child, meta):
        if len(child) == 1:
            result = child[0]
        else:
            result = {**child[1], "body": child[0]}
        return result

    def try_stmt(self, child, meta):
        result = {"type": "TRY", "lineno": meta.line, "linenoEnd": meta.end_line}
        if len(child) == 1:
            result = {**result, **child[0]}
        else:
            result = {**result, **child[1], "with": child[0]}
        return result

    def method(self, child, meta):
        result = {"lineno": meta.line, "linenoEnd": meta.end_line}
        if len(child) == 1:
            result = {**child[0], **result}
        else:
            result = {**child[1], "comment": child[0], **result}
        return result

    def method_annotations(self, child, meta):
        if len(child) == 1:
            result = child[0]
        else:
            result = {**child[1], "annotations": child[0]}
        return result

    def method_modifiers(self, child, meta):
        if len(child) == 1:
            result = child[0]
        else:
            result = {**child[1], "modifiers": child[0]}
        return result

    def method_return(self, child, meta):
        if len(child) == 1:
            result = {**child[0], "type": "CONSTRUCTOR"}
        else:
            result = {**child[1], "returnType": child[0], "type": "METHOD"}
        return result

    def method_name(self, child, meta):
        return {"name": child[0], **child[1]}

    def method_parameters(self, child, meta):
        if len(child) == 1:
            result = child[0]
        else:
            result = {**child[1], "parameters": child[0]}
        return result

    def method_throws(self, child, meta):
        result = {}
        for x in child:
            if type(x) == list:
                result["throws"] = x
            else:
                result = {**result, **x}
        return result

    def method_body(self, child, meta):
        result = {}
        if len(child) == 1:
            result["body"] = child[0]
        return result

    def block_modifier(self, child, meta):
        result = {"type": "BLOCK"}
        if len(child) == 1:
            result = {**child[0], **result}
        if len(child) == 2:
            result = {**child[1], "modifiers": child[0], **result}
            if "static" in child[0]:
                result["type"] = "STATIC_BLOCK"
        return result

    def block(self, child, meta):
        result = {
            "lineno": meta.line,
            "linenoEnd": meta.end_line,
        }
        if len(child) == 1:
            result = {**child[0], **result}
        if len(child) == 2:
            result = {**child[1], "comment": child[0], **result}
        return result
