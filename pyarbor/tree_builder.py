from pathlib import Path
from pathspec import PathSpec
from .file_parser import FileParser
from .node import Node, DirNode, FileNode


class DirectoryTreeBuilder:
    """Builds a tree structure of directories and optionally parses file contents."""

    def __init__(self, root_path: str, ignore_patterns: list[str] = []):
        self.root = Path(root_path).resolve()
        self.file_parser = FileParser()
        self.ignore_spec = PathSpec.from_lines("gitwildmatch", ignore_patterns)

    def build_tree(self) -> Node:
        """Recursively builds the directory and file tree."""
        self.root_node = self._build_node(self.root)
        return self.root_node

    def _build_node(self, path: Path) -> Node | None:
        """Internal method to traverse directories and create nodes."""

        # Skip files/directories that match ignore patterns
        if self.ignore_spec.match_file(str(path)):
            return None

        if path.is_dir():
            # Create a directory node
            dir_node = DirNode(path=str(path), children=[])
            for child in sorted(path.iterdir()):
                child_node = self._build_node(child)
                if child_node is not None:
                    dir_node.children.append(child_node)
            return dir_node
        else:
            # Handle files, either parsed or unparsed
            try:
                file_node = self.file_parser.parse_file(path)
            except Exception:
                # If parsing fails, create a node for the unparsed file
                file_content = None
                if path.is_file() and not path.is_symlink() and not path.is_socket():
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        file_content = f.read()
                file_node = FileNode(
                    path=str(path),
                    modified=path.stat().st_mtime_ns,
                    content=file_content,
                    children=[],
                )
            return file_node

    def update_tree(self, current_node: Node) -> Node | None:
        """Updates the tree to reflect the current file system state."""
        path = Path(current_node.path)

        # If the current path no longer exists, return None
        if not path.exists():
            return None

        if path.is_dir():
            # Update directory node
            children_paths = {child.path for child in current_node.children}
            actual_child_paths = {str(child.resolve()) for child in path.iterdir()}

            # Remove nodes for deleted files/directories
            current_node.children = [
                child
                for child in current_node.children
                if child.path in actual_child_paths
            ]

            # Update existing nodes recursively
            for child in current_node.children:
                updated_child = self.update_tree(child)
                if updated_child is not None:
                    current_node.children.remove(child)
                    current_node.children.append(updated_child)

            # Add new nodes for new files/directories
            new_paths = actual_child_paths - children_paths
            for new_path in new_paths:
                current_node.children.append(self._build_node(Path(new_path)))

        else:
            # Update file node if modified
            if path.stat().st_mtime_ns > current_node.modified:
                try:
                    current_node = self.file_parser.parse_file(path)
                except Exception:
                    file_content = None
                    if (
                        path.is_file()
                        and not path.is_symlink()
                        and not path.is_socket()
                    ):
                        with open(path, "r") as f:
                            file_content = f.read()
                    current_node.content = file_content
                    current_node.modified = path.stat().st_mtime_ns
            else:
                return None

        return current_node

    def get_node_by_path(
        self, path: Path, current_node: Node | None = None
    ) -> Node | None:
        """
        Fetch node for a given file path.

        Args:
            path (str): The absolute or relative path to the target file.
            current_node (Node): The current node in the tree to search from

        Returns:
            Node: The file node for the target file.

        Raises:
            FileNotFoundError: If the file does not exist in the tree.
        """
        if current_node is None:
            current_node = self.root_node

        if current_node.path == str(path):
            return current_node

        for child in current_node.children:
            if child.path == str(path):
                return child
            elif child.path in str(path):
                return self.get_node_by_path(path, child)
            else:
                raise RuntimeError("Should not reach here")

        return None
