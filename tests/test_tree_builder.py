from pyarbor.tree_builder import DirectoryTreeBuilder


def test_directory_tree_structure(tmp_path):
    # Create a mock file structure
    (tmp_path / "dir1").mkdir()
    (tmp_path / "dir1" / "file1.py").write_text("print('Hello')")
    (tmp_path / "dir2").mkdir()

    builder = DirectoryTreeBuilder(tmp_path)
    tree = builder.build_tree()

    print(tree)

    assert tree["type"] == "directory"
    assert len(tree["children"]) == 2
    assert any(child["name"] == "dir1" for child in tree["children"])

