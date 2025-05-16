import pytest
from jsx_parser.jsx_parser import JSXParser


@pytest.fixture
def parser():
    return JSXParser()


def test_simple_element(parser):
    jsx = '<div className="test">Hello</div>'
    result = parser.parse(jsx)
    assert result["type"] == "Element"
    assert result["tag"] == "div"
    assert result["attributes"] == {"className": "test"}
    assert len(result["children"]) == 1
    assert result["children"][0]["type"] == "Text"
    assert result["children"][0]["content"] == "Hello"


def test_self_closing_element(parser):
    jsx = '<input type="text" />'
    result = parser.parse(jsx)
    assert result["type"] == "Element"
    assert result["tag"] == "input"
    assert result["attributes"] == {"type": "text"}
    assert result["children"] == []


def test_nested_elements(parser):
    jsx = """
        <div className="container">
            <h1>Title</h1>
            <p>Content</p>
        </div>
    """
    result = parser.parse(jsx)
    assert result["type"] == "Element"
    assert result["tag"] == "div"
    assert result["attributes"] == {"className": "container"}
    assert len(result["children"]) == 2
    assert result["children"][0]["tag"] == "h1"
    assert result["children"][1]["tag"] == "p"


def test_multiple_attributes(parser):
    jsx = '<button type="submit" className="btn" disabled="true" />'
    result = parser.parse(jsx)
    assert result["type"] == "Element"
    assert result["tag"] == "button"
    assert result["attributes"] == {
        "type": "submit",
        "className": "btn",
        "disabled": "true",
    }
