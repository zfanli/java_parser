"""
Common.
"""

from lark import Transformer, v_args


@v_args(meta=True)
class CommonTransformer(Transformer):
    def path(self, child, _):

        return ".".join(child)
