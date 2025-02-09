from setuptools import setup, find_packages

setup(
    name="PyArbor",
    version="0.1.0",
    description="A directory parser with syntax-aware file parsing using Tree-sitter.",
    author="Your Name",
    license="MIT",
    packages=find_packages(where="pyarbor"),
    install_requires=["tree-sitter", "click"],
    tests_require=["pytest"],
    entry_points={"console_scripts": ["pyarbor=pyarbor.cli:main"]},
    include_package_data=True,
)

