"""
Method.
"""

from lark import Transformer, v_args


@v_args(meta=True)
class FieldTransformer(Transformer):
    def field(self, child, meta):
        if len(child) == 1:
            result = child[0]
        else:
            result = {**child[1], "comment": child[0]}
        # Convert body into name
        if "body" in result:
            result["name"] = result["body"]
            del result["body"]
        return {
            **result,
            "type": "FIELD",
            "lineno": meta.line,
            "linenoEnd": meta.end_line,
        }

    def field_annotation(self, child, _):
        if len(child) == 1:
            result = child[0]
        else:
            result = {**child[1], "annotations": child[0]}
        return result

    def fields(self, child, meta):
        return child
