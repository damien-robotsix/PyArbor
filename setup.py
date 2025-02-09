from setuptools import setup, find_packages

setup(
    name="pyarbor",
    version="0.1.0",
    description="A directory parser with syntax-aware file parsing using Tree-sitter.",
    author="Your Name",
    license="MIT",
    packages=find_packages(include=["pyarbor"]),
    install_requires=["pytest", "tree-sitter", "click", "tree-sitter-python"],
    entry_points={"console_scripts": ["pyarbor=pyarbor.cli:main"]},
    include_package_data=True,
)
