"""
Annotation.
"""

from lark import Transformer, v_args


@v_args(meta=True)
class AnnotationTransformer(Transformer):
    def annotation(self, child, meta):
        result = {
            "name": child[0],
            "lineno": meta.line,
            "linenoEnd": meta.end_line,
            "type": "ANNOTATION",
        }
        if len(child) == 2:
            result["args"] = child[1]
        return result

    def anno_arg_kv(self, child, _):
        if len(child) == 1:
            result = child[0]
        else:
            value = child[1]
            if type(value) != dict or (
                "type" in value and value["type"] == "ANNOTATION"
            ):
                value = {"value": value}
            result = {"key": child[0], **value}
        return result

    def anno_arg_list(self, child, _):
        result = "{}"
        if len(child) == 1:
            if type(child[0]) == list:
                result = {"value": child[0]}
            else:
                result = child[0]
        return result
