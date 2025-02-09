import pytest
from pyarbor.file_parser import FileParser
from pathlib import Path

def test_parse_python_file(tmp_path):
    # Create a mock Python file
    python_file = tmp_path / "example.py"
    python_file.write_text("def hello():\n    print('world')")

    parser = FileParser()
    result = parser.parse_file(python_file)

    assert "function_definition" in result["type"].lower()
    assert "hello" in result["text"].lower()