from pyarbor.file_parser import FileParser


def test_parse_python_file(tmp_path):
    # Create a mock Python file
    python_file = tmp_path / "example.py"
    python_file.write_text("def hello():\n    print('world')")

    parser = FileParser()
    result = parser.parse_file(python_file)

    assert result.path.endswith("example.py")
    assert result.content.root_node.children[0].type.lower() == "function_definition"
    assert b"def hello()" in result.content.root_node.children[0].text.lower()


def test_parse_markdown_file(tmp_path):
    # Create a mock Markdown file
    markdown_file = tmp_path / "example.md"
    markdown_file.write_text("# Title\n\nThis is a paragraph in a markdown file.")

    parser = FileParser()
    result = parser.parse_file(markdown_file)

    assert result.path.endswith("example.md")
    assert "document" in result.content.root_node.type.lower()
    assert b"# Title" in result.content.root_node.text
    assert b"This is a paragraph in a markdown file." in result.content.root_node.text


def test_parse_md_file(tmp_path):
    # Create a mock Markdown file
    md_file = tmp_path / "example.md"
    md_file.write_text("# Title\nThis is a test.")

    parser = FileParser()
    result = parser.parse_file(md_file)

    # Verify the parsed content
    assert b"Title" in result.content.root_node.text
    assert b"This is a test." in result.content.root_node.text


def test_parse_c_file(tmp_path):
    # Create a mock C file
    c_file = tmp_path / "example.c"
    c_file.write_text(
        """
        #include <stdio.h>

        void greet() {
            printf("Hello, World!");
        }

        int main() {
            greet();
            return 0;
        }
        """
    )

    parser = FileParser()
    result = parser.parse_file(c_file)

    # Verify the parsed content
    functions = [
        child
        for child in result.content.root_node.children
        if "function_definition" in child.type.lower()
    ]
    function_declarators = [function.children[1].text for function in functions]

    assert b"greet()" in function_declarators
    assert b"main()" in function_declarators


def test_parse_cpp_file(tmp_path):
    # Create a mock C++ file
    cpp_file = tmp_path / "example.cpp"
    cpp_file.write_text(
        """
        #include <iostream>
        using namespace std;

        class Greeter {
        public:
            void greet() {
                cout << "Hello, World!" << endl;
            }
        };

        int main() {
            Greeter g;
            g.greet();
            return 0;
        }
        """
    )

    parser = FileParser()
    result = parser.parse_file(cpp_file)

    # Verify the parsed content
    functions = [
        child
        for child in result.children
        if "function_definition" in child.type.lower()
    ]
    function_declarators = [function.children[1].text for function in functions]

    assert b"main()" in function_declarators
