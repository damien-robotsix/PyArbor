from pathlib import Path
from tree_sitter import Language, Parser
import tree_sitter_python


class FileParser:
    """Parses file content using Tree-sitter."""

    def __init__(self):
        PY_LANGUAGE = Language(tree_sitter_python.language())
        self.python_parser = Parser(PY_LANGUAGE)

    def parse_file(self, file_path: Path) -> dict:
        """Parse the file content based on its type."""
        ext = file_path.suffix[1:]
        if ext != "py":
            return {"error": f"No parser available for {ext} files."}

        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()

        try:
            tree = self.python_parser.parse(bytes(code, "utf-8"))
            return self._parse_tree(tree.root_node, code)
        except Exception as e:
            return {"error": str(e)}

    def _parse_tree(self, node, code: str) -> dict:
        """Recursively extract the Abstract Syntax Tree."""
        return {
            "type": node.type,
            "text": code[node.start_byte : node.end_byte],
            "children": [self._parse_tree(child, code) for child in node.children],
        }
