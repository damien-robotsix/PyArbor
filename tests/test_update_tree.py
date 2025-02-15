import pytest
from pyarbor.tree_builder import DirectoryTreeBuilder
from pyarbor.node import FileNode
from time import sleep


def test_update_tree(tmp_path):
    # Step 1: Create initial mock file and directory structure
    (tmp_path / "dir1").mkdir()
    (tmp_path / "dir1" / "file1.py").write_text("print('Hello')")
    (tmp_path / "dir2").mkdir()

    # Build the initial tree
    builder = DirectoryTreeBuilder(tmp_path)
    tree = builder.build_tree()

    sleep(0.1)
    # Step 2: Modify the file structure.

    # Modify an existing file
    (tmp_path / "dir1" / "file1.py").write_text("print('Hello, World!')")

    # Remove an existing directory
    (tmp_path / "dir2").rmdir()

    # Add new file and directory
    (tmp_path / "dir3").mkdir()
    (tmp_path / "dir3" / "file2.py").write_text("print('New File')")

    # Step 3: Update the tree
    updated_tree = builder.update_tree(tree)

    # Step 4: Assert updates are reflected

    # Check the updated tree structure
    assert (
        len(updated_tree.children) == 2
    )  # Should reflect "dir1" and "dir3", "dir2" is removed

    # Verify "dir1" remains and check its content
    dir1 = next(child for child in updated_tree.children if child.path.endswith("dir1"))
    assert len(dir1.children) == 1
    file1 = dir1.children[0]
    assert isinstance(file1, FileNode)
    assert file1.path.endswith("file1.py")
    assert file1.children[0].text == b"print('Hello, World!')"

    # Verify "dir3" is added and check its content
    dir3 = next(child for child in updated_tree.children if child.path.endswith("dir3"))
    assert len(dir3.children) == 1
    file2 = dir3.children[0]
    assert isinstance(file2, FileNode)
    assert file2.path.endswith("file2.py")
    assert file2.children[0].text == b"print('New File')"

    # Verify "dir2" is removed
    assert not any(child.path.endswith("dir2") for child in updated_tree.children)


if __name__ == "__main__":
    pytest.main()

