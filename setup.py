from setuptools import setup, find_packages

setup(
    name="pyarbor",
    version="0.1.0",
    description="A directory parser with syntax-aware file parsing using Tree-sitter.",
    author="Damien SIX <damien@robotsix.net>",
    license="MIT",
    packages=find_packages(include=["pyarbor"]),
    install_requires=[
        "pathspec",
        "tree-sitter==0.24.0",
        "tree-sitter-python",
        "tree-sitter-c==0.23.4",
        "tree-sitter-cpp==0.23.4",
        "tree-sitter-markdown==0.3.2",
        "tree-sitter-json",
        "tree-sitter-yaml",
    ],
    include_package_data=True,
)
