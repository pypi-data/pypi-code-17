from grako.exceptions import FailedParse

from prax import parser
from prax import praxidike


# noinspection PyMethodMayBeStatic
class PraxSemantics:
    def __init__(self, target, src=None, operators=None):
        self.src = src
        self.target = target
        self.operators = operators

    def expression(self, ast):
        result = ast.head
        for node in ast.tail:
            op = node[0]
            rhs = node[1]
            if '+' == op:
                result += rhs
        return result

    def term(self, ast):
        result = ast.head
        for node in ast.tail:
            ops = node[0]
            rhs = node[1]
            if '*' == ops:
                result *= self.target._to_int(rhs)
            if '@' == ops:
                start = self.target._to_int(result)
                count = self.target._to_int(rhs)
                result = "".join(
                    [self.target._to_str(x)
                     for x in range(start, start + count)])
        return result

    def literal(self, ast):
        ast = ast.replace("\\", "")
        if self.src is not None:
            val = self.src.parse(ast)
        else:
            val = praxidike.parse_to_int(ast)
        if self.operators is not None:
            val = self.operators(val)
        return self.target._to_str(val)


def main():
    try:
        parsy = parser.PraxParser(semantics=PraxSemantics(praxidike.Ascii))
        while True:
            try:
                text = input('> ')
                if text:
                    print(parsy.parse(text))
            except FailedParse:
                print("Invalid Syntax")
    except EOFError:
        pass
    except KeyboardInterrupt:
        print()
    print('bye')


if __name__ == "__main__":
    main()
