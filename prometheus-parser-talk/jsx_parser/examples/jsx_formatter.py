from dataclasses import dataclass
from typing import List, Optional
from jsx_parser import JSXParser


@dataclass
class JSXNode:
    tag: str
    attributes: dict
    children: List["JSXNode"]
    text: Optional[str] = None


class JSXFormatter:
    def __init__(self, indent_size: int = 4):
        self.indent_size = indent_size

    def format(self, node: JSXNode, level: int = 0) -> str:
        """Format a JSX AST node with proper indentation and spacing."""
        indent = " " * (level * self.indent_size)

        # Handle text-only nodes
        if node.text is not None and not node.children:
            return f"{indent}{node.text.strip()}"

        # Start building the opening tag
        result = [f"{indent}<{node.tag}"]

        # Add formatted attributes
        if node.attributes:
            attrs = []
            for key, value in sorted(node.attributes.items()):
                attrs.append(f'{key}="{value}"')
            result.append(" " + " ".join(attrs))

        if not node.children and not node.text:
            # Self-closing tag
            result.append(" />")
            return "".join(result)

        result.append(">")

        # Handle children
        if node.children:
            result.append("\n")
            for child in node.children:
                result.append(self.format(child, level + 1))
                result.append("\n")
            result.append(indent)
        elif node.text:
            # Handle text content
            result.append(node.text.strip())

        # Add closing tag
        result.append(f"</{node.tag}>")

        return "".join(result)


def format_jsx(ast: JSXNode, indent_size: int = 4) -> str:
    """
    Format JSX AST with consistent spacing and indentation.

    Args:
        ast: The JSX AST to format
        indent_size: Number of spaces to use for each indentation level

    Returns:
        A formatted string representation of the JSX
    """
    formatter = JSXFormatter(indent_size=indent_size)
    return formatter.format(ast)


def convert_ast(parser_ast):
    """Convert parser AST format to formatter AST format."""
    if not parser_ast:
        return None

    if parser_ast["type"] == "Element":
        children = [convert_ast(child) for child in parser_ast.get("children", [])]
        children = [child for child in children if child is not None]

        return JSXNode(
            tag=parser_ast["tag"],
            attributes=parser_ast.get("attributes", {}),
            children=children,
            text=None,
        )
    else:  # Text node
        return JSXNode(tag="", attributes={}, children=[], text=parser_ast["content"])


def main():
    """Example usage of the JSX formatter with raw JSX inputs."""
    parser = JSXParser()

    raw_examples = [

        """<div>  Hello    World  </div>""",

        """<button type = "submit"disabled="true"    className  =  "btn-primary">
            Click   Me
        </button>""",

        """<div className="container"><header>
        <h1 className="title">Welcome</h1><nav><ul>
        <li>Home</li><li>About</li>
            <li>Contact</li>
                </ul></nav>
        </header><main>
            <article><h2>Title</h2><p>Content goes here</p></article></main></div>""",
    ]

    for i, raw_jsx in enumerate(raw_examples, 1):
        print(f"Example {i}:")
        print("---------- INPUT JSX ----------")
        print(raw_jsx)

        ast = parser.parse(raw_jsx)
        formatted_ast = convert_ast(ast)
        formatted = format_jsx(formatted_ast)

        print("\nFormatted Output:")
        print("---------- OUTPUT JSX ----------")
        print(formatted)
        print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    main()
