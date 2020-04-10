"""
Class.
"""

from lark import Transformer, v_args


@v_args(meta=True)
class ClassTransformer(Transformer):
    def clazz(self, child, meta):
        if len(child) == 1:
            result = child[0]
        else:
            result = {**child[1], "fileComment": child[0]}
        return result

    def class_package(self, child, meta):
        if len(child) == 1:
            result = child[0]
        else:
            result = {**child[1], "package": child[0]}
        return result

    def class_imports(self, child, meta):
        if len(child) == 1:
            result = child[0]
        else:
            result = {**child[1], "imports": child[0]}
        return result

    def class_comment(self, child, meta):
        result = {"lineno": meta.line, "linenoEnd": meta.end_line}
        if len(child) == 1:
            result = {**child[0], **result}
        else:
            result = {**child[1], "comment": child[0], **result}
        return result

    def class_annotations(self, child, meta):
        if len(child) == 1:
            result = child[0]
        else:
            result = {**child[1], "annotations": child[0]}
        return result

    def class_modifier(self, child, meta):
        if len(child) == 1:
            result = child[0]
        else:
            result = {**child[1], "modifiers": child[0]}
        return result

    def class_identity(self, child, meta):
        return {"type": child[0].upper(), **child[1]}

    def class_identifier(self, child, meta):
        return {"name": child[0], **child[1]}

    def class_extends(self, child, meta):
        if len(child) == 1:
            result = child[0]
        else:
            result = {**child[1], "superclasses": child[0]}
        return result

    def class_interfaces(self, child, meta):
        if len(child) == 1:
            result = child[0]
        else:
            result = {**child[1], "interfaces": child[0]}
        return result

    def class_throws(self, child, meta):
        if len(child) == 1:
            result = child[0]
        else:
            result = {**child[1], "throws": child[0]}
        return result

    def class_body(self, child, meta):
        result = {}
        fields = [
            x
            for x in child
            if type(x) == dict and x["type"] in {"FIELD", "ENUM_FIELD", "ENUM_ELEMENTS"}
        ]
        methods = [
            x
            for x in child
            if type(x) == dict and x["type"] in ("METHOD", "CONSTRUCTOR")
        ]
        if len(fields) > 0:
            result["fields"] = fields
        if len(methods) > 0:
            result["methods"] = methods
        return result
