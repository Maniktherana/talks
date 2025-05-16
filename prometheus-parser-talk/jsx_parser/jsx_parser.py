from .jsx_lexer import JSXLexer


class JSXParser:
    def __init__(self):
        self.lexer = JSXLexer().build()
        self.current_token = None

    def parse(self, data):
        self.lexer.input(data)
        self.advance()
        return self.parse_element()

    def advance(self):
        """Move to the next token."""
        self.current_token = self.lexer.token()
        return self.current_token

    def expect(self, token_type):
        """Verify the current token is of expected type and advance."""
        if self.current_token and self.current_token.type == token_type:
            token = self.current_token
            self.advance()
            return token
        raise SyntaxError(
            f"Expected {token_type}, got {self.current_token.type if self.current_token else 'EOF'}"
        )

    def parse_element(self):
        if not self.current_token:
            return None

        if self.current_token.type == "TEXT":
            node = {"type": "Text", "content": self.current_token.value}
            self.advance()
            return node

        if self.current_token.type == "TAGSTART":
            self.advance()
            tag_name = self.expect("IDENTIFIER").value
            attributes = self.parse_attributes()

            if self.current_token.type == "SELFCLOSING":
                self.advance()
                return {
                    "type": "Element",
                    "tag": tag_name,
                    "attributes": attributes,
                    "children": [],
                }

            self.expect("TAGEND")
            children = self.parse_children()

            self.expect("CLOSETAG")
            closing_tag = self.expect("IDENTIFIER").value
            if closing_tag != tag_name:
                raise SyntaxError(
                    f"Mismatched tags: opening '{tag_name}' and closing '{closing_tag}'"
                )
            self.expect("TAGEND")

            return {
                "type": "Element",
                "tag": tag_name,
                "attributes": attributes,
                "children": children,
            }

        return None

    def parse_attributes(self):
        attributes = {}
        while self.current_token and self.current_token.type == "IDENTIFIER":
            attr_name = self.current_token.value
            self.advance()
            self.expect("EQUALS")
            attr_value = self.expect("STRING").value
            attributes[attr_name] = attr_value
        return attributes

    def parse_children(self):
        children = []
        while self.current_token and self.current_token.type not in ("CLOSETAG", None):
            child = self.parse_element()
            if child:
                children.append(child)
        return children


if __name__ == "__main__":
    parser = JSXParser()
    test_jsx = """
        <div className="container">
            <h1>Hello World</h1>
            <Button type="submit" />
        </div>
    """
    result = parser.parse(test_jsx)
    print("Parsed JSX:", result)
