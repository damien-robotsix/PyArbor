from pydantic import BaseModel, Field, ConfigDict
from tree_sitter import Tree, Node as TSNode
from datetime import datetime


class Node(BaseModel):
    """Represents a directory or file node in the tree structure."""

    model_config: ConfigDict = {
        "arbitrary_types_allowed": True,
    }

    path: str = Field(..., title="Path to the node")
    type: str = Field(..., title="Type of the node")
    children: list["Node | TSNode"] = Field([], title="List of child nodes")


Node.model_rebuild


class DirNode(Node):
    """Represents a directory node in the tree structure."""

    type: str = "directory"


class FileNode(Node):
    """Represents a file node in the tree structure."""

    type: str = "file"
    modified: datetime = Field(..., title="Last modified timestamp of the file")
    content: str | Tree | None = Field(
        ..., title="Content of the file as a string (not parsed) or Tree-sitter Tree"
    )
