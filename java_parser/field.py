"""
Method.
"""

from lark import Transformer, v_args


@v_args(meta=True)
class FieldTransformer(Transformer):
    def field(self, child, meta):

        return {}
