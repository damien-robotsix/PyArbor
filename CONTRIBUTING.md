# Contributing to PyArbor

Thank you for considering contributing to PyArbor! Here are some guidelines to help you:

## Getting Started
1. Fork the repository and clone it to your local machine.
2. Make sure you have Python 3.7 or higher installed.

## Installing the Development Environment
1. Create a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Install the package in editable mode:

    ```bash
    pip install -e .
    ```

## Running Tests
Run the test suite with:

```bash
pytest tests/
```

## Submitting Changes
1. Create a feature branch for your changes:

    ```bash
    git checkout -b my-feature
    ```

2. Commit and push your changes to your fork.
3. Submit a pull request to the `main` branch in the upstream repository.

## Code Style
Ensure your code adheres to PEP8 standards. You can use tools like `black` and `flake8`:

```bash
pip install black flake8
black .
flake8 .
```

## Reporting Issues
If you encounter bugs or have suggestions, please open a GitHub issue with details.

Thank you for contributing!