from pyarbor.file_parser import FileParser


def test_parse_python_file(tmp_path):
    # Create a mock Python file
    python_file = tmp_path / "example.py"
    python_file.write_text("def hello():\n    print('world')")

    parser = FileParser()
    result = parser.parse_file(python_file)

    result = result["children"][0]
    assert "function_definition" in result["type"].lower()
    assert "hello" in result["text"].lower()


def test_parse_markdown_file(tmp_path):
    # Create a mock Markdown file
    markdown_file = tmp_path / "example.md"
    markdown_file.write_text("# Title\n\nThis is a paragraph in a markdown file.")

    parser = FileParser()
    result = parser.parse_file(markdown_file)

    assert "document" in result["type"].lower()
    assert "# Title" in result["text"]
    assert "This is a paragraph in a markdown file." in result["text"]


def test_parse_txt_file(tmp_path):
    # Create a mock TXT file
    txt_file = tmp_path / "example.txt"
    txt_file.write_text("This is a test.")

    parser = FileParser()
    result = parser.parse_file(txt_file)

    # Verify the parsed text
    assert "This is a test." in result["text"]


def test_parse_md_file(tmp_path):
    # Create a mock Markdown file
    md_file = tmp_path / "example.md"
    md_file.write_text("# Title\nThis is a test.")

    parser = FileParser()
    result = parser.parse_file(md_file)

    # Verify the parsed content
    assert "Title" in result["text"]
    assert "This is a test." in result["text"]
