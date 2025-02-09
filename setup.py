from setuptools import setup, find_packages

setup(
    name="pyarbor",
    version="0.1.0",
    description="A directory parser with syntax-aware file parsing using Tree-sitter.",
    author="Damien SIX <damien@robotsix.net>",
    license="MIT",
    packages=find_packages(include=["pyarbor"]),
    install_requires=[
        "tree-sitter==0.24.0",
        "click",
        "tree-sitter-python",
        "tree-sitter-c==0.23.4",
        "tree-sitter-cpp==0.23.4",
        "tree-sitter-markdown==0.3.2",
    ],
    entry_points={"console_scripts": ["pyarbor=pyarbor.cli:main"]},
    include_package_data=True,
)
