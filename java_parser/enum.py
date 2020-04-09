"""
Enum.
"""

from lark import Transformer, v_args


@v_args(meta=True)
class EnumTransformer(Transformer):
    def enum_class_elem(self, child, meta):
        return {
            "body": child,
            "type": "ENUM_ELEMENTS",
            "lineno": meta.line,
            "linenoEnd": meta.end_line,
        }

    def enum_field(self, child, meta):
        result = {"type": "ENUM_FIELD", "lineno": meta.line, "linenoEnd": meta.end_line}
        if len(child) == 1:
            result = {**child[0], **result}
        else:
            result = {**child[1], "comment": child[0], **result}
        return result

    def enum_field_modifiers(self, child, _):
        if len(child) == 1:
            result = child[0]
        else:
            result = {**child[1], "modifiers": child[0]}
        return result

    def enum_field_name(self, child, meta):
        return {"name": child[0], **child[1]}

    def enum_field_body(self, child, meta):
        return {"body": child[0]}

    def enum_elem(self, child, meta):
        result = {
            "type": "ENUM_ELEMENT",
            "lineno": meta.line,
            "linenoEnd": meta.end_line,
        }
        if len(child) == 1:
            result = {**child[0], **result}
        else:
            result = {**child[1], "comment": child[0], **result}
        return result

    def enum_elem_name(self, child, meta):
        return {"name": child[0], **child[1]}

    def enum_elem_args(self, child, _):
        if len(child) == 1:
            result = child[0]
        else:
            result = {"args": child[0], **child[1]}
        return result

    def enum_elem_body(self, child, _):
        result = {}
        if len(child) > 0:
            result["body"] = child
        return result
