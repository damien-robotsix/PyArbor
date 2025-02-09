import click
import json
from .tree_builder import DirectoryTreeBuilder


@click.command()
@click.argument("path", type=click.Path(exists=True))
@click.option(
    "--output", "-o", type=click.Choice(["json", "text"]), default="json", help="Output format"
)
def main(path, output):
    """CLI for PyArbor: Parse directory structure and optionally file content."""
    builder = DirectoryTreeBuilder(path)
    tree = builder.build_tree()

    if output == "json":
        print(json.dumps(tree, indent=4))
    elif output == "text":
        _print_text_tree(tree)


def _print_text_tree(node, indent=0):
    """Helper function to print a directory tree in text format."""
    prefix = "  " * indent + ("📂 " if node.get("type") == "directory" else "📄 ")
    print(f"{prefix}{node['name']}")
    if node.get("children"):
        for child in node["children"]:
            _print_text_tree(child, indent + 1)


if __name__ == "__main__":
    main()