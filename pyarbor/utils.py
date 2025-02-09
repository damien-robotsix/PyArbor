import json

def save_to_json_file(data, file_path):
    """Save data to a JSON file."""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def read_from_json_file(file_path):
    """Read data from a JSON file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def format_path(path):
    """Format and normalize a file system path."""
    import os
    return os.path.normpath(os.path.abspath(path))