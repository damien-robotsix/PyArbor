from pathlib import Path
import importlib
from typing import Dict, Optional
from tree_sitter import Parser, Language
from .node import FileNode


class LangConfig:
    """Dynamically loads Tree-sitter language modules and maps them to file extensions."""

    _EXTENSION_MAP = {
        "tree_sitter_python": [".py"],
        "tree_sitter_c": [".c", ".h"],
        "tree_sitter_cpp": [".cpp", ".hpp", ".cc"],
        "tree_sitter_markdown": [".md"],
        "tree_sitter_json": [".json"],
        "tree_sitter_yaml": [".yaml", ".yml"],
    }

    def __init__(self):
        self.languages: Dict[str, Language] = {}
        self.extension_to_lang: Dict[str, str] = {}
        self._load_languages()

    @property
    def supported_extensions(self):
        """Returns a list of supported file extensions."""
        return list(self.extension_to_lang.keys())

    def get_language(self, ext: str) -> Optional[Language]:
        """Returns the appropriate Tree-sitter Language object for a file extension."""
        lang_name = self.extension_to_lang.get(ext)
        return self.languages.get(lang_name) if lang_name is not None else None

    def _load_languages(self):
        """Dynamically loads Tree-sitter language modules and initializes parsers."""
        for lang_prefix in self._EXTENSION_MAP.keys():
            try:
                # Dynamically import the module for the language
                module = importlib.import_module(lang_prefix)
                lang = Language(module.language())
                self.languages[lang_prefix] = lang

                # Map extensions to their respective language modules
                for ext in self._EXTENSION_MAP[lang_prefix]:
                    self.extension_to_lang[ext] = lang_prefix
            except ImportError:
                # Ignore languages that are not available
                continue


LANG_CONFIG = LangConfig()


class FileParser:
    """Manages the parsing of files using the Tree-sitter library."""

    def __init__(self):
        self.parser = None

    # TODO: parse file with old tree
    def parse_file(self, file_path: Path) -> Optional[FileNode]:
        """Parses a file and returns a FileNode representation."""
        ext = file_path.suffix
        tree_sitter_lang = LANG_CONFIG.get_language(ext)

        if not tree_sitter_lang:
            return None  # Unsupported language for parsing

        self.parser = Parser(tree_sitter_lang)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                file_content = f.read()

            tree = self.parser.parse(bytes(file_content, "utf-8"))
            return FileNode(
                path=str(file_path),
                modified=file_path.stat().st_mtime_ns,
                content=tree,
                children=tree.root_node.children,
            )
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return None
