"""
Annotation.
"""

from lark import Transformer, v_args


@v_args(meta=True)
class AnnotationTransformer(Transformer):
    def annotation(self, child, meta):

        child = child[0]

        return {
            "annotation": child,
            "lineno": meta.line,
            "linenoEnd": meta.end_line,
        }
