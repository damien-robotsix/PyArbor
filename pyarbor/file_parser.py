from pathlib import Path
from tree_sitter import Language, Parser
import tree_sitter_python
import tree_sitter_c
import tree_sitter_cpp
import tree_sitter_markdown
import json
import yaml


class FileParser:
    """Parses file content using Tree-sitter or appropriate libraries."""

    def __init__(self):
        # Initialize Tree-sitter language parsers
        PY_LANGUAGE = Language(tree_sitter_python.language())
        C_LANGUAGE = Language(tree_sitter_c.language())
        CPP_LANGUAGE = Language(tree_sitter_cpp.language())
        MD_LANGUAGE = Language(tree_sitter_markdown.language())
        self.parsers = {
            "py": Parser(PY_LANGUAGE),
            "c": Parser(C_LANGUAGE),
            "cpp": Parser(CPP_LANGUAGE),
            "md": Parser(MD_LANGUAGE),
        }

    def parse_file(self, file_path: Path) -> dict:
        """Parse the file content based on its type."""
        ext = file_path.suffix[1:]  # Extract file extension

        if ext in self.parsers:
            # Handle Tree-sitter supported languages (Python, C, C++, Markdown)
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()

            try:
                parser = self.parsers[ext]
                tree = parser.parse(bytes(code, "utf-8"))
                return self._parse_tree(tree.root_node, code)
            except Exception as e:
                return {"error": str(e)}

        elif ext == "json":
            # JSON parsing
            return self._parse_json(file_path)

        elif ext == "yaml":
            # YAML parsing
            return self._parse_yaml(file_path)

        elif ext == "txt":
            # Plain text parsing
            return self._parse_text(file_path)

        else:
            return {"error": f"No parser available for {ext} files."}

    def _parse_tree(self, node, code: str) -> dict:
        """Recursively extract the Abstract Syntax Tree."""
        return {
            "type": node.type,
            "text": code[node.start_byte : node.end_byte],
            "children": [self._parse_tree(child, code) for child in node.children],
        }

    def _parse_json(self, file_path: Path) -> dict:
        """Parse JSON files."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            return {"error": str(e)}

    def _parse_yaml(self, file_path: Path) -> dict:
        """Parse YAML files."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except Exception as e:
            return {"error": str(e)}

    def _parse_text(self, file_path: Path) -> dict:
        """Process plain text files."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return {"text": f.read()}
        except Exception as e:
            return {"error": str(e)}
