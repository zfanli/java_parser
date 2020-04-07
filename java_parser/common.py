"""
Common.
"""

from lark import Transformer, v_args


def operator_pair(target):
    chain = []
    for x in filter(lambda x: x % 2 != 1, range(len(target))):
        op = target[x]
        right = target[x + 1]
        chain.append({"value": right, "operator": str(op)})
    return chain


@v_args(meta=True)
class CommonTransformer(Transformer):
    def new(self, _, __):
        return "new"

    def true(self, _, __):
        return True

    def false(self, _, __):
        return False

    def null(self, _, __):
        return None

    def path(self, child, _):
        return ".".join(child)

    def dotted_name(self, child, _):
        return ".".join(child)

    def comment(self, child, _):
        return [str(x) for x in child]

    def name(self, child, _):
        (child,) = child
        return str(child)

    def star(self, child, _):
        (child,) = child
        return str(child)

    def boolean(self, child, _):
        (child,) = child
        return child

    def number(self, child, _):
        (child,) = child
        return float(child)

    def string(self, child, _):
        (child,) = child
        return child.replace('\\"', '"')

    def primary(self, child, _):
        (child,) = child
        return child

    def cast_type(self, child, _):
        (child,) = child
        return child

    def generic_type(self, child, _):

        if len(child) == 0:
            child = ["<>"]

        return {"value": child}

    def class_type(self, child, _):

        value = child[0]
        result = value
        if len(child) == 2:
            result = {"value": child[0], "generic": child[1]}

        return result

    def getattr(self, child, _):
        if len(child) == 2:
            base = child[0]
            name = child[1]
        else:
            base = child[0]
            name = f"<{child[1]}> {child[2]}"

        if type(base) == str:
            result = ".".join([base, name])
        else:
            result = {"base": base, "name": name, "type": "ATTRIBUTE"}
        return result

    def getitem(self, child, _):
        (name, index) = child
        return f"{name}[{int(index)}]"

    def arguments(self, child, _):
        return child

    def funccall(self, child, meta):

        result = {"name": child[0], "type": "INVOCATION"}
        if len(child) == 2:
            result["args"] = child[1]

        return result

    def test(self, child, meta):

        left = child[0]
        middle = None
        right = None
        result = {"value": left}

        if len(child) == 3:
            middle = child[1]
            right = child[2]
            result = {
                "condition": left,
                "ifTrue": middle,
                "ifFalse": right,
                "type": "TERNARY_EXPRESSION",
            }

        return result

    def or_test(self, child, _):

        left = child[0]
        result = {"value": left}
        if len(child) > 1:
            rest = child[1:]
            result = {"left": left, "right": rest, "type": "TEST_OR"}

        return result

    def and_test(self, child, _):

        left = child[0]
        result = {"value": left}
        if len(child) > 1:
            rest = child[1:]
            result = {"left": left, "right": rest, "type": "TEST_AND"}

        return result

    def not_test(self, child, _):
        (child,) = child
        return child

    def not_test_body(self, child, _):

        left = child[0]
        result = {"value": left, "type": "TEST_NOT"}

        return result

    def comparison(self, child, _):

        left = child[0]
        result = {"value": left}
        if len(child) > 1:
            rest = child[1:]
            chain = operator_pair(rest)
            result = {"left": left, "chain": chain, "type": "COMPARISON"}

        return result

    def xor_expr(self, child, _):
        return {"value": child, "type": "XOR_EXPRESSION"}

    def expr(self, child, _):
        return {"value": child, "type": "BITWISE_OR"}

    def and_expr(self, child, _):
        return {"value": child, "type": "BITWISE_AND"}

    def shift_expr(self, child, _):
        left = child[0]
        result = {"value": left}
        if len(child) > 1:
            rest = child[1:]
            chain = operator_pair(rest)
            result = {"left": left, "chain": chain, "type": "SHIFT_EXPRESSION"}

        return result

    def arith_expr(self, child, _):
        left = child[0]
        result = {"value": left}
        if len(child) > 1:
            rest = child[1:]
            chain = operator_pair(rest)
            result = {"left": left, "chain": chain, "type": "ARITHMETIC_EXPRESSION"}

        return result

    def term(self, child, _):
        left = child[0]
        result = {"value": left}
        if len(child) > 1:
            rest = child[1:]
            chain = operator_pair(rest)
            result = {"left": left, "chain": chain, "type": "ARITHMETIC_EXPRESSION"}

        return result

    def power(self, child, _):
        left = child[0]
        result = {"value": left}
        if len(child) == 2:
            result = {"value": left, "power": int(child[1]), "type": "POWER_EXPRESSION"}
        return result

    def new_expr(self, child, _):
        if len(child) == 1:
            result = child[0]
        else:
            result = {"value": child[1], "type": "NEW_EXPRESSION"}
        return result

    def cast_expr(self, child, _):
        if len(child) == 1:
            result = child[0]
        else:
            result = {"value": child[1], "cast": child[0], "type": "CAST_EXPRESSION"}
        return result
