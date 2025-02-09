from pathlib import Path
from .file_parser import FileParser


class DirectoryTreeBuilder:
    """Builds a tree structure of directories and optionally parses file contents."""

    def __init__(self, root_path: str):
        self.root = Path(root_path).resolve()
        self.file_parser = FileParser()

    def build_tree(self) -> dict:
        """Recursively builds the directory and file tree."""
        return self._build_node(self.root)

    def _build_node(self, path: Path) -> dict:
        """Internal method to traverse directories and create nodes."""
        node = {
            "name": path.name,
            "path": str(path),
            "type": "directory" if path.is_dir() else "file",
            "children": [] if path.is_dir() else None,
        }

        if path.is_dir():
            for child in sorted(path.iterdir()):
                node["children"].append(self._build_node(child))
        else:
            node["content"] = self.file_parser.parse_file(path)

        return node