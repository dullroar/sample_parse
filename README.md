# sample-parse

A simple, elegant utility for parsing strings to their intended Python types. It intelligently detects and converts strings to JSON objects, Python literals, regex patterns, floats, integers, or falls back to plain strings.

## Features

- **Smart Type Detection**: Automatically converts strings to the most appropriate Python type
- **JSON Support**: Parses JSON objects, arrays, and primitives
- **Pythonic Literals**: Handles Python-specific types like tuples, sets, and `None`
- **Regex Patterns**: Recognizes and compiles regular expressions
- **Number Parsing**: Supports decimals, floats, hex, octal, and binary integers
- **CLI Tool**: Includes a command-line interface for easy testing
- **Zero Dependencies** (core library): The parsing library has no external dependencies; the CLI optional requires Click

## Installation

### From source
```bash
cd sample
pip install -e .
```

### With development dependencies
```bash
pip install -e ".[dev]"
```

## Quick Start

### See it in action

```bash
python examples.py
```

This runs interactive examples showing the parser handling JSON, numbers, regex, Python literals, and edge cases—perfect for getting a feel for the module.

### Use as a library

```python
from sample import parse_string_to_typed

# Parse JSON
result = parse_string_to_typed('{"key": "value"}')
# → {'key': 'value'}

# Parse numbers
result = parse_string_to_typed('42')
# → 42

result = parse_string_to_typed('3.14')
# → 3.14

# Parse booleans
result = parse_string_to_typed('true')
# → True

# Parse regex patterns
result = parse_string_to_typed('/[a-z]+/')
# → re.compile('[a-z]+')

# Fallback to string
result = parse_string_to_typed('hello')
# → 'hello'
```

### Command-Line Interface

The CLI provides convenient access to the parsing functionality:

#### Parse a single value
```bash
sample parse "123"
# Output: int: 123

sample parse '{"key": "value"}'
# Output: dict: {'key': 'value'}

sample parse "3.14"
# Output: float: 3.14

sample parse "/[a-z]+/"
# Output: Pattern: /[a-z]+/
```

#### Parse multiple values
```bash
sample parse-batch "123" "3.14" '{"key": "value"}'
```

#### Output as JSON
```bash
sample parse "123" --json
# Output: 123

sample parse '{"key": "value"}' --json
# Output: {
#   "key": "value"
# }
```

## Parsing Strategy

The function attempts type coercion in this order:

1. **JSON** - Strict JSON objects, arrays, and primitives
2. **Pythonic Literals** - Tuples, sets, Python-specific keywords (True, False, None)
3. **Regex Patterns** - Strings wrapped in `/pattern/` or containing regex metacharacters
4. **Float** - Decimal numbers like `3.14`, `1e10`, etc.
5. **Integer** - Whole numbers in decimal, hex (`0xFF`), octal (`0o77`), or binary (`0b101`)
6. **String** - If none of the above match, returns the original string

## Testing

The project uses **pytest** for modern, idiomatic Python testing with parametrized test cases.

### Quick start

```bash
# Run all tests
pytest tests/ -v

# Run tests with coverage report
pytest tests/ --cov=sample --cov-report=html

# Run a specific test class
pytest tests/test_common.py::TestJsonParsing -v

# Run with coverage report
pytest tests/ --cov=sample --cov-report=term-missing
```

### Test suite organization

**89 total tests** organized into:
- **73 parametrized test cases** covering all parsing pathways:
  - JSON (objects, arrays, primitives, numbers)
  - Python literals (tuples, sets, True/False, None)
  - Regex patterns (with and without delimiters)
  - Numbers (floats, integers, hex, octal, binary)
  - Edge cases and fallbacks

- **16 organized integration tests** by category:
  - `TestJsonParsing` - JSON object/array/primitive parsing
  - `TestRegexParsing` - Regex pattern recognition and compilation
  - `TestNumberParsing` - Float and integer parsing (hex/octal/binary)
  - `TestEdgeCases` - Empty strings, whitespace, invalid input fallbacks
  - `TestPythonLiterals` - Tuples, sets, Python keywords

**Result:** 100% pass rate, 10.00/10 pylint rating

## Project Structure

```
sample/
├── sample/                          # Main package
│   ├── __init__.py                 # Package initialization
│   ├── common.py                   # Core parsing logic
│   └── cli.py                      # Click-based CLI
├── tests/                          # Test suite (pytest)
│   ├── __init__.py
│   ├── conftest.py                 # pytest configuration and fixtures
│   └── test_common.py              # 89 parametrized and integration tests
├── .vscode/                        # VS Code workspace settings
│   └── settings.json               # Pylint configuration for VS Code
├── examples.py                     # Quick-start examples (run this first!)
├── .pylintrc                       # Pylint configuration
├── pyproject.toml                  # Modern Python project config (PEP 517/518)
├── requirements.txt                # Dependencies
├── README.md                       # This file
├── LICENSE                         # MIT License
└── .gitignore                      # Git ignore patterns
```

## Development

### Set up development environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"
```

### Run examples

See the module in action with practical examples:

```bash
python examples.py
```

### Run tests

```bash
# Run all tests with verbose output
pytest tests/ -v

# Run specific test class
pytest tests/test_common.py::TestJsonParsing -v

# Run with coverage report
pytest tests/ --cov=sample --cov-report=html
```

### Code quality tools

```bash
# Linting (configured in .pylintrc)
pylint sample/ tests/ examples.py

# Code formatting
black sample/ tests/ examples.py
isort sample/ tests/ examples.py

# Type checking
mypy sample/
```

### Code style

The project uses:
- **Pylint** for linting (rating: 10.00/10) - configured in `.pylintrc`
- **Black** for code formatting (88 char line length)
- **isort** for import organization
- **mypy** for static type checking
- **Pytest** for testing with parametrized test cases

Configuration suppresses trivial style warnings (C0303, C0304) for developer experience.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

## Author

Your Name - [your.email@example.com](mailto:your.email@example.com)
