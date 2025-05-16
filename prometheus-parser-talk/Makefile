.PHONY: install format test all clean help print-ast format-jsx

install:
	uv venv venv
	. venv/bin/activate && uv pip install -e ".[dev]"

format:
	venv/bin/ruff format .

print-ast:
	venv/bin/python -m jsx_parser.examples.print_ast

format-jsx:
	venv/bin/python -m jsx_parser.examples.jsx_formatter

test:
	venv/bin/python -m pytest

clean:
	rm -rf venv .ruff_cache __pycache__ .pytest_cache 