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
    def list(self, child, _):
        return child

    def literal(self, child, _):
        (child,) = child
        return str(child)

    def itself(self, child, _):
        return child[0]

    def ellipsis(self, _, __):
        return "..."

    def new(self, _, __):
        return "new"

    def true(self, _, __):
        return True

    def false(self, _, __):
        return False

    def null(self, _, __):
        return None

    def dotjoin(self, child, _):
        return ".".join(child)

    def concatjoin(self, child, _):
        return "".join(child)

    def comment(self, child, _):
        return [str(x) for x in child]

    def comment_inline(self, child, _):
        return str(child[0])

    def number(self, child, _):
        (child,) = child
        return float(child)

    def string(self, child, _):
        (child,) = child
        return child.replace('\\"', '"')

    def generic_type(self, child, _):
        (child,) = child
        if type(child) != list:
            child = [str(child)]
        return child

    def class_type(self, child, _):

        result = child[0]
        if len(child) == 2:
            if type(result) == dict:
                result["arraySuffix"] = child[1]
            else:
                result = {"name": result, "arraySuffix": child[1]}

        return result

    def class_ellipsis(self, child, _):

        result = child[0]
        if len(child) == 2:
            if type(result) == dict:
                result["name"] = result["name"] + "..."
            else:
                result = result + "..."

        return result

    def class_generic(self, child, _):

        result = child[0]
        if len(child) == 2:
            result = {"name": child[0], "generic": child[1]}

        return result

    def getattr(self, child, _):
        if len(child) == 2:
            base = child[0]
            name = child[1]
        else:
            base = child[0]
            name = f"<{','.join(child[1])}> {child[2]}"

        if type(base) == str:
            result = ".".join([base, name])
        else:
            result = {"base": base, "name": name, "type": "ATTRIBUTE"}
        return result

    def getitem(self, child, _):
        return {"name": child[0], "index": child[1], "type": "ARRAY_OPERATION"}

    def funccall(self, child, _):

        result = {"name": child[0], "type": "INVOCATION"}
        if len(child) == 2:
            result["args"] = child[1]

        return result

    def arrayliteral(self, child, _):

        result = {"name": child[0], "type": "ARRAY_LITERAL"}
        if len(child) == 2:
            result["value"] = child[1]

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

    def argvalue(self, child, _):
        if len(child) == 1:
            result = child[0]
        else:
            result = {"key": child[0], "value": child[1], "type": "KEY_VALUE_PAIR"}
        return result

    def parameter(self, child, _):
        if len(child) == 2:
            result = {"name": child[1], "classType": child[0], "type": "PARAMETER"}
        else:
            result = {
                "name": child[2],
                "classType": child[1],
                "annotations": child[0],
                "type": "PARAMETER",
            }
        return result

    def factor(self, child, _):
        if len(child) == 1:
            result = child[0]
        else:
            op = child[0]
            rest = child[1]
            result = {"value": rest, "operator": str(op), "type": "FACTOR_EXPRESSION"}
        return result

    def binary_bf(self, child, _):
        if len(child) == 1:
            result = child[0]
        else:
            op = child[0]
            rest = child[1]
            result = {
                "value": rest,
                "operator": str(op),
                "type": "BINARY_BEFORE_EXPRESSION",
            }
        return result

    def binary_af(self, child, _):
        if len(child) == 1:
            result = child[0]
        else:
            op = child[1]
            rest = child[0]
            result = {
                "value": rest,
                "operator": str(op),
                "type": "BINARY_AFTER_EXPRESSION",
            }
        return result

    def lambda_expr(self, child, meta):
        return {
            **child[0],
            **child[1],
            "type": "LAMBDA_EXPRESSION",
            "lineno": meta.line,
            "linenoEnd": meta.end_line,
        }

    def lambda_param(self, child, _):
        result = {}
        if len(child) == 1:
            param = child[0]
            if type(param) == str:
                param = [param]
            result = {"parameters": param}
        return result

    def lambda_body(self, child, _):
        result = {}
        if len(child) == 1:
            body = child[0]
            if type(body) == dict:
                body = [body]
            result = {"body": body}
        return result

    def return_type(self, child, _):
        if len(child) == 1:
            result = child[0]
        else:
            result = {"generic": child[0], "name": child[1]}
        return result
