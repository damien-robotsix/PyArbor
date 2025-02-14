from pathlib import Path
from .file_parser import FileParser
from .node import Node, DirNode, FileNode


class DirectoryTreeBuilder:
    """Builds a tree structure of directories and optionally parses file contents."""

    def __init__(self, root_path: str):
        self.root = Path(root_path).resolve()
        self.file_parser = FileParser()

    def build_tree(self) -> Node:
        """Recursively builds the directory and file tree."""
        return self._build_node(self.root)

    def _build_node(self, path: Path) -> Node:
        """Internal method to traverse directories and create nodes."""

        if path.is_dir():
            # Create a directory node
            dir_node = DirNode(path=str(path), children=[])
            for child in sorted(path.iterdir()):
                dir_node.children.append(self._build_node(child))
            return dir_node
        else:
            # Handle files, either parsed or unparsed
            try:
                file_node = self.file_parser.parse_file(path)
            except Exception:
                # If parsing fails, create a node for the unparsed file
                # File content is loaded if file in not a binary
                file_content = None
                if path.is_file() and not path.is_symlink() and not path.is_socket():
                    with open(path, "r") as f:
                        file_content = f.read()
                file_node = FileNode(
                    path=str(path), modified=path.stat().st_mtime, content=file_content
                )
            return file_node
