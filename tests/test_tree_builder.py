from pyarbor.tree_builder import DirectoryTreeBuilder
from pathlib import Path


def test_directory_tree_structure(tmp_path):
    # Create a mock file structure
    (tmp_path / "dir1").mkdir()
    (tmp_path / "dir1" / "file1.py").write_text("print('Hello')")
    (tmp_path / "dir2").mkdir()

    builder = DirectoryTreeBuilder(tmp_path)
    tree = builder.build_tree()

    assert tree.path == str(tmp_path)
    assert len(tree.children) == 2
    assert any(child.path.endswith("dir1") for child in tree.children)

    dir1 = next(child for child in tree.children if child.path.endswith("dir1"))

    file1 = next(child for child in dir1.children if child.path.endswith("file1.py"))
    assert file1.content.root_node.children[0].type == "expression_statement"


if __name__ == "__main__":
    test_directory_tree_structure(Path("/tmp/my_test"))
