"""
Modifiers.
"""

from lark import Transformer, v_args


@v_args(meta=True)
class ModifierTransformer(Transformer):
    def private(self, _, __):
        return "private"

    def public(self, _, __):
        return "public"

    def protected(self, _, __):
        return "protected"

    def default(self, _, __):
        return "default"

    def final(self, _, __):
        return "final"

    def static(self, _, __):
        return "static"

    def transient(self, _, __):
        return "transient"

    def synchronized(self, _, __):
        return "synchronized"

    def volatile(self, _, __):
        return "volatile"

    def abstract(self, _, __):
        return "abstract"
