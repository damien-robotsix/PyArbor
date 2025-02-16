from pyarbor.tree_builder import DirectoryTreeBuilder
from pathlib import Path


def test_directory_tree_structure(tmp_path):
    # Create a mock file structure
    (tmp_path / "dir1").mkdir(exist_ok=True)
    (tmp_path / "dir1" / "file1.py").write_text("print('Hello')")
    (tmp_path / "dir2").mkdir(exist_ok=True)

    builder = DirectoryTreeBuilder(tmp_path)
    tree = builder.build_tree()

    assert tree.path == str(tmp_path)
    assert len(tree.children) == 2
    assert any(child.path.endswith("dir1") for child in tree.children)

    dir1 = next(child for child in tree.children if child.path.endswith("dir1"))

    file1 = next(child for child in dir1.children if child.path.endswith("file1.py"))
    assert file1.content.root_node.children[0].type == "expression_statement"


def test_get_node_by_path(tmp_path):
    # Create a mock directory and file
    file_path = tmp_path / "test_file.py"
    file_path.write_text("print('Hello')")  # Sample content

    builder = DirectoryTreeBuilder(tmp_path)
    builder.build_tree()
    node = builder.get_node_by_path(file_path)

    # Check that tree represents a valid Node
    assert node is not None
    assert node.content.root_node is not None


if __name__ == "__main__":
    test_directory_tree_structure(Path("/tmp/my_test"))
    test_get_node_by_path(Path("/tmp/my_test"))
