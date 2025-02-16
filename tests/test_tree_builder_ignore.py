from pyarbor.tree_builder import DirectoryTreeBuilder


def test_ignore_patterns(tmp_path):
    # Set up a mock file structure
    (tmp_path / "dir1").mkdir()
    (tmp_path / "dir1" / "file1.py").write_text("# Sample Python script")
    (tmp_path / "__pycache__").mkdir()
    (tmp_path / "__pycache__" / "cached.pyc").write_text("# Cached file")

    # Initialize with ignore patterns
    builder = DirectoryTreeBuilder(tmp_path, ignore_patterns=["__pycache__", "*.py"])
    tree = builder.build_tree()
    dir1 = next(child for child in tree.children if child.path.endswith("dir1"))
    # Assert `__pycache__` and `*.pyc` files are excluded
    assert not any(child.path.endswith("__pycache__") for child in tree.children)
    assert not any(child.path.endswith("file1.py") for child in dir1.children)


def test_no_ignore(tmp_path):
    # Set up a mock file structure
    (tmp_path / "dir1").mkdir()
    (tmp_path / "dir1" / "file1.py").write_text("# Sample Python script")
    (tmp_path / "__pycache__").mkdir()
    (tmp_path / "__pycache__" / "cached.pyc").write_text("# Cached file")

    # Initialize without ignore parameters
    builder = DirectoryTreeBuilder(tmp_path)
    tree = builder.build_tree()

    # Assert everything is included
    assert any(child.path.endswith("__pycache__") for child in tree.children)
    dir1 = next(child for child in tree.children if child.path.endswith("dir1"))
    assert any(child.path.endswith("file1.py") for child in dir1.children)
    pycache = next(
        child for child in tree.children if child.path.endswith("__pycache__")
    )
    assert any(child.path.endswith("cached.pyc") for child in pycache.children)

