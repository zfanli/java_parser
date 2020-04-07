"""
Annotation.
"""

from lark import Transformer, v_args


@v_args(meta=True)
class AnnotationTransformer(Transformer):
    def annotation(self, child, meta):

        value = child[0]

        result = {
            "value": value,
            "lineno": meta.line,
            "linenoEnd": meta.end_line,
            "type": "ANNOTATION",
        }

        if len(child) == 2:
            result["param"] = child[1]

        return result

    def anno_param_kv(self, child, _):
        key, value = (child[0], child[1])
        return {
            "key": key,
            "value": value,
        }

    def anno_param_kv_list(self, child, _):
        if len(child) == 1:
            key = "<default>"
            value = child[0]
        else:
            key, value = (child[0], child[1])
        return {
            "key": key,
            "value": value,
        }

    def anno_param_base(self, child, _):
        (child,) = child
        return child

    def anno_param_list(self, child, _):
        return child

    def anno_params(self, child, _):
        return child

    def anno_param(self, child, _):
        return child
