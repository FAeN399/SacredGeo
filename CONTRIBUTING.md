# Contributing to Advanced Sacred Geometry

Thank you for your interest in contributing to the Advanced Sacred Geometry project! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and considerate of others when contributing to this project. We aim to foster an inclusive and welcoming community.

## How to Contribute

There are many ways to contribute to this project:

1. **Report bugs**: If you find a bug, please create an issue with a detailed description of the problem, steps to reproduce it, and your environment.
2. **Suggest features**: If you have an idea for a new feature or enhancement, please create an issue to discuss it.
3. **Improve documentation**: Help improve the documentation by fixing typos, adding examples, or clarifying explanations.
4. **Submit code**: Contribute code by fixing bugs, implementing features, or improving existing code.

## Development Setup

1. Fork the repository on GitHub.
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/sacred-geometry.git
   cd sacred-geometry
   ```
3. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev]"
   ```
4. Create a branch for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Guidelines

### Code Style

We follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide for Python code. You can use tools like `flake8` and `black` to check and format your code:

```bash
flake8 sacred_geometry
black sacred_geometry
```

### Testing

Please write tests for your code. We use `pytest` for testing:

```bash
pytest
```

To run tests with coverage:

```bash
pytest --cov=sacred_geometry
```

### Documentation

- Document your code using docstrings following the [NumPy docstring style](https://numpydoc.readthedocs.io/en/latest/format.html).
- Update the README.md and other documentation files as needed.
- Add examples to demonstrate new features.

## Pull Request Process

1. Update your fork to the latest version of the main repository.
2. Make your changes in a new branch.
3. Run tests and ensure they pass.
4. Update documentation as needed.
5. Submit a pull request to the main repository.
6. Describe your changes in the pull request description.
7. Wait for review and address any feedback.

## Adding New Sacred Geometry Patterns

When adding new sacred geometry patterns or shapes:

1. Add the implementation in the appropriate module (core, shapes, fractals, etc.).
2. Add tests for the new pattern.
3. Add documentation with mathematical background and cultural significance.
4. Add examples demonstrating the new pattern.
5. Update the GUI to include the new pattern if applicable.

## License

By contributing to this project, you agree that your contributions will be licensed under the project's MIT License.

## Questions?

If you have any questions about contributing, please open an issue or contact the maintainers.

Thank you for your contributions!
