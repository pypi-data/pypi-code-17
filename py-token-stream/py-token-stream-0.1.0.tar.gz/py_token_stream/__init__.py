class TokenStream:

    def __init__(self, tokens):
        self.tokens = tokens

    def lookahead(self, index):
        return self.tokens[index]

    def peek(self):
        return self.tokens[0]

    def advance(self):
        return self.tokens.pop(0)

    def defer(self, token):
        self.tokens.insert(0, token)
