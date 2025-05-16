from jsx_parser import JSXParser


class ASTPrinter:
    def __init__(self, indent_size: int = 2):
        self.indent_size = indent_size

    def print(self, ast, level: int = 0) -> None:
        """Pretty print an AST node with proper indentation."""
        if not ast:
            return

        indent = " " * (level * self.indent_size)
        if ast["type"] == "Element":
            print(f"{indent}{ast['type']}: <{ast['tag']}>")
            if ast["attributes"]:
                print(f"{indent}Attributes:", ast["attributes"])
            if ast["children"]:
                print(f"{indent}Children:")
                for child in ast["children"]:
                    self.print(child, level + 1)
        else:
            print(f"{indent}Text: '{ast['content']}'")


def print_ast(ast, indent_size: int = 2) -> None:
    """
    Pretty print a JSX AST with consistent indentation.
    """
    printer = ASTPrinter(indent_size=indent_size)
    printer.print(ast)


def main():
    """Example usage of the AST printer with different JSX inputs."""
    parser = JSXParser()

    examples = [
        "<div>Hello World</div>",
        '<button type="submit" className="btn">Click me</button>',
        """
        <div className="container">
            <h1>Title</h1>
            <p>Some content</p>
            <button type="button" />
        </div>
        """,
    ]

    for i, jsx in enumerate(examples, 1):
        print(f"Example {i}:")
        print("---------- INPUT JSX ----------")
        print(jsx)
        print("---------- AST STRUCTURE ----------")
        ast = parser.parse(jsx)
        print_ast(ast)
        print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    main()
