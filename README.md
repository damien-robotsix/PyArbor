# PyArbor

PyArbor is a Python package that provides tools for recursively parsing a directory structure and analyzing file contents using Tree-sitter. It outputs the results as a structured tree in either JSON or text formats.

## Features
- Recursive directory traversal.
- Syntax-aware file parsing for supported file types.
- Outputs directory and file structures in JSON or text formats.

## Installation
To install PyArbor, first ensure Python 3.7 or higher is installed. Then run:

```bash
pip install .
```

Or install directly from the repository:

```bash
pip install git+<repository-url>
```

## Usage
Use the command-line interface to parse a directory:

```bash
pyarbor /path/to/directory --output json
```

For text output:

```bash
pyarbor /path/to/directory --output text
```

## Contributing
Contributions are welcome! Please see `CONTRIBUTING.md` for guidelines on how to contribute to this project.

## License
This project is licensed under the MIT License - see the `LICENSE` file for details.
