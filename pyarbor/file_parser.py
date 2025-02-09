from pathlib import Path
from tree_sitter import Language, Parser


class FileParser:
    """Parses file content using Tree-sitter."""

    def __init__(self):
        # Initialize parsers for Python
        self.parsers = {}
        PY_LANGUAGE_PATH = "path/to/tree-sitter-python"
        Language.build_library(
            'build/my-languages.so',
            [PY_LANGUAGE_PATH]
        )
        PY_LANGUAGE = Language('build/my-languages.so', 'python')

        self.parsers['py'] = Parser()
        self.parsers['py'].set_language(PY_LANGUAGE)

    def parse_file(self, file_path: Path) -> dict:
        """Parse the file content based on its type."""
        ext = file_path.suffix[1:]  # File extension (e.g., 'py', 'js')
        if ext not in self.parsers:
            return {"error": f"No parser available for {ext} files."}

        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()

        try:
            parser = self.parsers[ext]
            tree = parser.parse(bytes(code, "utf8"))
            root_node = tree.root_node
            return self._parse_tree(root_node, code)
        except Exception as e:
            return {"error": str(e)}

    def _parse_tree(self, node, code: str) -> dict:
        """Recursively extract the Abstract Syntax Tree."""
        return {
            "type": node.type,
            "text": code[node.start_byte:node.end_byte],
            "children": [self._parse_tree(child, code) for child in node.children],
        }