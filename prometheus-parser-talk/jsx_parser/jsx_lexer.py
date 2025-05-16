from ply import lex


class JSXLexer:
    # List of token names
    tokens = (
        "TAGSTART",  # <
        "TAGEND",  # >
        "CLOSETAG",  # </
        "SELFCLOSING",  # />
        "EQUALS",  # =
        "STRING",  # "hello" or 'hello'
        "IDENTIFIER",  # tag names, attribute names
        "TEXT",  # text content
    )

    t_INITIAL_ignore = " \t\n"
    t_text_ignore = " \t\n"

    states = (("text", "exclusive"),)

    # Tokens
    def t_ANY_error(self, t):
        t.lexer.skip(1)

    def t_INITIAL_SELFCLOSING(self, t):
        r"/>"
        return t

    def t_INITIAL_CLOSETAG(self, t):
        r"</"
        return t

    def t_INITIAL_TAGSTART(self, t):
        r"<(?!/)"
        return t

    def t_INITIAL_TAGEND(self, t):
        r">"
        t.lexer.begin("text")
        return t

    def t_INITIAL_EQUALS(self, t):
        r"="
        return t

    def t_INITIAL_STRING(self, t):
        r'"[^"]*"|\'[^\']*\''
        t.value = t.value[1:-1]
        return t

    def t_INITIAL_IDENTIFIER(self, t):
        r"[a-zA-Z][a-zA-Z0-9_-]*"
        return t

    def t_text_TEXT(self, t):
        r"[^<]+"
        t.value = t.value.strip()
        if t.value:
            return t

    def t_text_CLOSETAG(self, t):
        r"</"
        t.lexer.begin("INITIAL")
        return t

    def t_text_TAGSTART(self, t):
        r"<(?!/)"
        t.lexer.begin("INITIAL")
        return t

    def t_text_whitespace(self, t):
        r"[ \t\n]+"
        pass

    def t_whitespace(self, t):
        r"[ \t\n]+"
        pass

    def t_newline(self, t):
        r"\n+"
        t.lexer.lineno += len(t.value)

    t_ignore = " \t"

    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
        t.lexer.skip(1)

    def t_text_error(self, t):
        print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
        t.lexer.skip(1)

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        return self.lexer

    def tokenize(self, data):
        self.lexer.input(data)
        return [t for t in self.lexer]


if __name__ == "__main__":
    lexer = JSXLexer().build()
    test_data = """
        <div className="container">
            <h1>Hello World</h1>
            <Button type="submit" />
        </div>
    """
    lexer.input(test_data)
    for token in lexer:
        print(token)
