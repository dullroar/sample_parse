<!-- This file is LONG. Read it in sections or search for what interests you. -->

# Learn Modern Python Development Through sample-parse

A comprehensive, opinionated guide to contemporary Python development practices as exemplified by the `sample-parse` project. Written for experienced software engineers and architects ramping up on modern Python culture.

**Table of Contents**
1. [Philosophy & Project Context](#philosophy--project-context)
2. [Project Structure: The Why](#project-structure-the-why)
3. [Dependency Management: Earned Complexity](#dependency-management-earned-complexity)
4. [Testing as a First-Class Citizen](#testing-as-a-first-class-citizen)
5. [Code Quality & Linting](#code-quality--linting)
6. [Distribution & Package Management](#distribution--package-management)
7. [Development Workflow](#development-workflow)
8. [Real-World Lessons](#real-world-lessons)

---

## Philosophy & Project Context

### The Historical Context

You've likely lived through the evolution of packaging and dependency management across languages. Python has had a **chaotic history**:

- **Before 2020s**: setuptools, `setup.py`, `setup.cfg`, various competing packaging tools (distutils, pip, conda, poetry, pipenv...)
- **2020 onwards**: **PEP 517/518/620** unified the ecosystem around `pyproject.toml`

The `sample-parse` project uses **modern conventions** (as of 2024-2026) which represent the Python ecosystem's consensus on how projects *should* be structured.

**Key References:**
- PEP 517: "A build-system independent format" - https://www.python.org/dev/peps/pep-0517/
- PEP 518: "Specifying build system requirements" - https://www.python.org/dev/peps/pep-0518/
- PEP 620: "Isolate from unsupported platform configurations" - https://www.python.org/dev/peps/pep-0620/
- Modern Python Packaging Landscape: https://packaging.python.org/

### What This Project Demonstrates

`sample-parse` is intentionally **small but complete**:
- **Minimal**: No framework complexity, no 50-layer abstraction
- **Production-ready**: Linting, testing, packaging, documentation
- **Modern**: Uses current best practices (2024+)
- **Realistic**: Mirrors how real Python projects are structured

It's a **reference architecture**, not a tutorial project. Every structural decision is deliberate.

---

## Project Structure: The Why

### Top-Level Directory Layout

```
sample-parse/
├── sample_parse/                  # The actual package (importable)
├── tests/                     # Test code (separate from package)
├── .vscode/                   # IDE configuration (team consistency)
├── .pylintrc                  # Linter configuration
├── pyproject.toml            # **Single source of truth for project metadata**
├── requirements.txt          # Pinned dependencies for reproducibility
├── examples.py               # Getting-started reference
├── README.md                 # User-facing documentation
└── LICENSE                   # Legal foundation
```

### Why NOT Have `src/sample/`?

Many Python projects use:
```
sample-parse/
├── src/
│   └── sample_parse/
├── tests/
```

**This project doesn't.** Why?

1. **Simpler imports during development**: Direct `import sample_parse` works without path manipulation
2. **Fewer layers of indirection**: Engineers are practical about complexity budgets
3. **Standard for small-to-medium projects**: The `src/` layout shines primarily for *massive* monorepos (like Django itself)
4. **Practice in this context**: For this learning project, the overhead isn't worth the benefit

**Trade-off**: If this grew into a large monorepo with multiple packages, the `src/` layout would become valuable for namespace isolation.

**Reference**: https://packaging.python.org/tutorials/packaging-projects/

### Inside `sample_parse/` (The Package)

```python
sample_parse/
├── __init__.py              # Makes it a package, exports public API
├── common.py                # Core logic
└── cli.py                   # Click CLI interface
```

#### Why This Organization?

Modern Python practice suggests:
- **One top-level `__init__.py`** that re-exports the public API
- **Internal modules** (like `common.py`, `cli.py`) for different concerns
- **Flat structure** for small packages (deep hierarchies harm readability)

**sample_parse/__init__.py**:
```python
"""sample: A utility for parsing strings to their intended Python types."""

__version__ = "0.1.0"
from .common import parse_string_to_typed

__all__ = ["parse_string_to_typed"]
```

This serves multiple purposes:
1. **Documents the public API**: Users see immediately what to import
2. **Version centralization**: Single source of truth for versioning
3. **Module documentation**: Package-level docstring visible to `help(sample)`
4. **Namespace cleanliness**: Extra imports (like `json`, `re`) stay internal to `common.py`

Why not expose CLI code? Because:
- CLI is an *interface*, not a feature library
- Users importing `sample_parse` want `parse_string_to_typed()`, not CLI machinery
- Separation of concerns: library logic ≠ shell interface

### Inside `tests/`

```
tests/
├── __init__.py              # Makes it a package (necessary for pytest discovery)
├── conftest.py              # pytest fixtures and configuration
└── test_common.py           # All tests for the application
```

#### Why Not `test_sample_parse.py`?

The module is named `test_common.py` because it tests `common.py`. If the project grew:

```
tests/
├── test_common.py           # Tests for common.py
├── test_cli.py              # Tests for cli.py
├── fixtures/
│   └── sample_data.py       # Shared test data
```

This mirrors the module structure: clarity and searchability.

#### Why Tests Are Separate

In some languages (Go, Rust), tests live alongside code:
```
rust/
├── src/
│   ├── lib.rs
│   └── main.rs
├── tests/                   # Separate directory for integration tests
```

Python convention places **unit tests separately**:

```
python/
├── sample_parse/                  # Importable package
│   └── __init__.py
├── tests/                   # NOT importable; pytest finds it
│   └── test_*.py
```

**Why?**
1. **Clean distribution**: When you release via PyPI, test code doesn't ship
2. **Psychological boundary**: Tests are development artifacts, not product
3. **IDE filtering**: Many IDEs hide `tests/` in tree views by default
4. **Pytest discovery**: The default `pytest` command finds `tests/test_*.py` automatically

**Reference**: https://docs.pytest.org/en/stable/how-to-organize-code.html

---

## Dependency Management: Earned Complexity

### The Three Files (and Why You Need Three)

This project has what looks redundant:
- `pyproject.toml` - Project metadata, build system, development dependencies
- `requirements.txt` - Pinned versions for reproducibility
- `setup.py` - Not present (intentionally modern)

#### `pyproject.toml`: The Constitution

This is the **single source of truth** for your project.

**Structure breakdown:**
```toml
[build-system]              # How to build this project
requires = ["setuptools>=65.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]                   # What this project *is*
name = "sample-parse"
version = "0.1.0"
description = "..."
requires-python = ">=3.8"
dependencies = ["click>=8.0.0"]

[project.optional-dependencies]  # Extra installation profiles
dev = ["pytest>=7.0", "black>=23.0", ...]

[project.scripts]           # Command-line entry points
sample = "sample.cli:cli"

[tool.black]                # Tool-specific configuration
line-length = 88

[tool.pytest.ini_options]   # pytest behavior
testpaths = ["tests"]
```

**Why `pyproject.toml` matters:**
- **PEP 517 compliance**: Any build tool (pip, poetry, flit, PDM) can build this
- **Single file principle**: All metadata lives here, not scattered across files
- **Tool standardization**: Black, pytest, mypy, isort all read from `pyproject.toml`
- **Reproducibility**: Version requirements are explicit

**Historical context**: Before 2020, this information was split across:
- `setup.py` (messy Python file)
- `setup.cfg` (INI-style configuration)
- `tox.ini` (testing configuration)
- Various tool-specific files

Modern Python consolidated this. The win is enormous.

**Reference**: https://pip.pypa.io/en/latest/reference/build-system/pyproject-toml/

#### `requirements.txt`: Pins for CI and Production

While `pyproject.toml` specifies *what* you need, `requirements.txt` pins *exact versions*:

```
click==8.1.7
pytest==7.4.2
black==23.11.0
```

**Why separate files?**

| Scenario | Use |
|----------|-----|
| Local dev: `pip install -e ".[dev]"` | Uses `pyproject.toml` (flexible versions) |
| CI/CD build: `pip install -r requirements.txt` | Uses `requirements.txt` (locked versions) |
| Production deployment | Uses `requirements.txt` (locked versions) |

**Philosophy**: 
- During development, you want *flexibility* ("give me pytest >= 7.0, I don't care about the minor version")
- In CI/production, you want *reproducibility* ("pytest == 7.4.2, exactly")

This is earned complexity: it solves real problems (dependency drift, environment differences).

**How to maintain `requirements.txt`:**
```bash
# Generate locked versions after updating pyproject.toml
pip install pip-tools
pip-compile --output-file=requirements.txt pyproject.toml
```

Or use newer tools:
- **PDM** (https://pdm-project.org/) - Modern replacement for pip
- **Poetry** (https://python-poetry.org/) - All-in-one dependency manager
- **uv** (https://github.com/astral-sh/uv) - Rust-based, extremely fast

Each has trade-offs; this project chose pip + pip-tools for simplicity.

#### Why No `setup.py`?

Traditionally, projects had a Python file for installation:
```python
# Old way (don't do this)
from setuptools import setup

setup(
    name="sample-parse",
    version="0.1.0",
    ...
)
```

**Problems:**
- Python files can do *anything* (hidden behavior, side effects)
- Build tools must execute arbitrary Python
- Not declarative; hard to introspect without running code
- Version from one place, dependencies from another

**Modern alternative** (`pyproject.toml`):
- Build-agnostic declaration
- Tools can read it without executing Python
- Single source of truth

If `setup.py` were needed (for custom build logic), it would be minimal:
```python
from setuptools import setup
setup()  # All config from pyproject.toml
```

This project doesn't need it.

---

## Testing as a First-Class Citizen

### Why Testing Is Taken Seriously Here

In many languages, testing is an afterthought. Python culture places testing at the **center of development**:
- Django ships with test framework built-in
- PyTest is universally adopted
- Test-driven development is normative
- Coverage reports are expected

This project has **89 tests for ~200 lines of code**. This ratio seems absurd until you understand the testing philosophy.

### Structure: `tests/conftest.py`

```python
# tests/conftest.py

@pytest.fixture
def sample_strings():
    """Fixture providing sample string test values."""
    return {
        "json_object": '{"key": "value"}',
        ...
    }

def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "json: mark test as testing JSON parsing")
```

**What's happening:**

1. **Fixtures** (`@pytest.fixture`): Reusable test data/setup
   - Instead of repeating test data in every test, define once
   - Pytest injects these into test functions automatically
   - Makes tests declarative and DRY

2. **Custom markers** (in `pytest_configure`):
   ```bash
   pytest tests/ -m json    # Run only JSON-related tests
   ```
   - Organizes tests by concern
   - Enables selective test runs

**Why this matters:**
- **Scale**: As projects grow, test infrastructure becomes critical
- **Clarity**: Tests read like specifications, not implementation
- **Maintainability**: Shared fixtures prevent duplication

**Reference**: https://docs.pytest.org/en/stable/how-to-parametrize.html

### Parametrized Tests: Test Explosion Without Code Explosion

The project has 73 parametrized test cases:

```python
# In test_common.py
PARSE_TEST_CASES = [
    ('{"key": "value"}', {"key": "value"}),
    ('{"a": 1, "b": 2}', {"a": 1, "b": 2}),
    ('{}', {}),
    # ... 70 more cases
]

class TestParseStringToTyped:
    @pytest.mark.parametrize("input_val,expected", PARSE_TEST_CASES)
    def test_parse(self, input_val: Any, expected: Any) -> None:
        result = parse_string_to_typed(input_val)
        assert _regex_equals(result, expected), ...
```

**What this accomplishes:**
- 1 test method × 73 cases = effective coverage
- Easy to add cases: append tuple to `PARSE_TEST_CASES`
- Pytest reports each case separately in verbose output
- Cases are data, not code (easier to maintain)

**Without parametrization**, you'd need 73 separate methods (nightmare to maintain).

**Historical context**: XUnit-style testing (Java, C#) required this boilerplate. Python's pytest made it elegant.

**Reference**: https://docs.pytest.org/en/stable/how-to-parametrize.html

### Test Organization: Integration Tests

Beyond parametrized cases, the project has integration tests:

```python
class TestJsonParsing:
    """Integration tests for JSON parsing."""
    
    def test_json_object(self) -> None:
        """JSON objects should be parsed to dicts."""
        assert parse_string_to_typed('{"key": "value"}') == {"key": "value"}

class TestRegexParsing:
    """Integration tests for regex pattern parsing."""
    
    def test_slash_delimited_regex(self) -> None:
        """Regex patterns with / / delimiters should be compiled."""
        result = parse_string_to_typed('/[a-z]+/')
        assert isinstance(result, type(re.compile('')))
```

**Why both parametrized + integration tests?**

| Type | Purpose |
|------|---------|
| **Parametrized** | Exhaustive coverage of single concern (all number formats, etc.) |
| **Integration** | Verify features work end-to-end |

Integration tests:
- Have docstrings explaining the feature
- Are readable as specification
- Verify behavior holistically (not isolated micro-cases)
- Often have more assertions and setup

**Trade-off**: Parametrized tests are efficient; integration tests are readable. Use both.

---

## Code Quality & Linting

### The Linting Stack

This project uses:
- **pylint** (primary style/quality checker) - https://www.pylint.org/
- **black** (code formatter) - https://github.com/psf/black
- **isort** (import sorter) - https://pycqa.github.io/isort/
- **mypy** (static type checker) - https://www.mypy-lang.org/

Why *four* tools for "quality"?

#### pylint: The Stern Teacher

pylint finds:
- Unused variables
- Unreachable code
- Variable naming conventions
- Logical errors
- Code complexity issues

**Rating system**: 10.00/10 is perfect. This project maintains 10.00/10.

Configuration in `.pylintrc`:

```ini
[DESIGN]
max-returns = 6           # Allow up to 6 return statements
max-statements = 50       # Allow up to 50 statements per function

[MESSAGES CONTROL]
disable = C0303,C0304     # Suppress trivial whitespace warnings
```

**Philosophy**: Linting isn't about perfection; it's about catching *patterns*:
- Variables declared but never used = likely bug
- Cyclomatic complexity > 15 = probably needs refactoring
- Magic numbers with no context = maintenance hazard

**vs. flake8**: Some projects use flake8 instead (simpler, fewer false positives). This project chose pylint for its comprehensive analysis.

#### black: Removing Style Debates

Code formatting wars are *unproductive*. Black enforces an **opinionated standard**:

```python
# Before: What you want
result = some_function_with_long_name(argument1, argument2, argument3, argument4)

# After: What black gives you
result = some_function_with_long_name(
    argument1, argument2, argument3, argument4
)
```

Black has **zero configuration** (except line length). This is intentional: the goal is to stop debating style.

**Integration**: In modern workflows:
```bash
black sample_parse/ tests/ examples.py    # Format in place
```

Or integrated into editor (VS Code via Pylance/Python extension).

#### isort: Import Organization

Python has no consensus on import order. isort enforces:

```python
# Standard library
import json
import re

# Third-party
import click

# Local
from .common import parse_string_to_typed
```

Why order matters:
- **Readability**: You scan imports to understand dependencies
- **Reducesmerge conflicts**: Consistent order means fewer diffs
- **Signals intent**: Standard > third-party > local (clear dependency hierarchy)

**PEP 8** recommends this order; isort enforces it automatically.

#### mypy: Static Typing Without Forced Runtime Enforcement

Python is **dynamically typed**, but accepts type hints:

```python
def parse_string_to_typed(value: str) -> Any:
    """..."""
    if not isinstance(value, str):
        return value
    ...
```

mypy reads these hints and checks for type inconsistencies:

```python
result: int = parse_string_to_typed("hello")  # Error: returns str, not int
```

Benefits:
- **Catch bugs before runtime**: Type mismatches found at development time
- **Better IDE support**: Autocomplete knows the type signature
- **Documentation**: Function signature is self-documenting
- **No runtime cost**: Type hints are *optional* and ignored at runtime

**Philosophy**: Python typing is not Java's compile-time enforcement. It's *optional*. This project adds types incrementally where they help.

**Reference**: https://www.python.org/dev/peps/pep-0484/

### Configuration in One Place

All tool configuration lives in `pyproject.toml`:

```toml
[tool.black]
line-length = 88
target-version = ['py38', 'py39', 'py310', 'py311']

[tool.isort]
profile = "black"

[tool.mypy]
python_version = "3.8"
warn_return_any = true
```

**Why?** Single source of truth. Developers, CI/CD, and IDEs all read the same config.

### Pylint: The Outlier

Wait, why is pylint configured in `.pylintrc` instead of `pyproject.toml`?

Historical reasons: pylint was slow to adopt `pyproject.toml` (as of 2024, it's improving). For this project, we use both:
- `.pylintrc` for pylint-specific settings
- `pyproject.toml` for other tools

**Real-world note**: Many teams disable pylint entirely and rely on:
- Black (formatting)
- mypy (types)
- Ruff (fast linting) - https://github.com/astral-sh/ruff

Ruff is newer, faster, and increasingly popular. For this learning project, pylint demonstrates comprehensive linting.

---

## Distribution & Package Management

### How to Share This Project

#### Option 1: Development Install (Local)

```bash
pip install -e .
```

This installs the package in **editable mode**:
- Code changes are immediately reflected
- You can `import sample_parse` as if it's installed
- Great for development

#### Option 2: PyPI Distribution (Production)

```bash
# Build distributable
python -m build

# This creates:
# dist/sample_parse-0.1.0.tar.gz      (source distribution)
# dist/sample_parse-0.1.0-py3-none-any.whl  (wheel)

# Upload to PyPI
twine upload dist/*
```

**What's a wheel?** A precompiled binary format (like a JAR in Java). Faster to install than source distributions.

**Reference**: https://packaging.python.org/tutorials/packaging-projects/

### Versioning Strategy

This project uses **semantic versioning** (MAJOR.MINOR.PATCH):

```
0.1.0  =  MAJOR.MINOR.PATCH
│   │      │      │       └─ Patch: bug fixes (0.1.1)
│   │      │      └───────── Minor: new features (0.2.0)
│   └──────└────────────────  Major: breaking changes (1.0.0)
```

Specified in one place: `__init__.py` (or `pyproject.toml`):

```python
__version__ = "0.1.0"
```

Best practice: automate version extraction during build (e.g., setuptools_scm), but for small projects, manual is fine.

---

## Development Workflow

### Local Development Setup

```bash
# Clone project
git clone <repo>
cd sample-parse

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install in editable mode with development dependencies
pip install -e ".[dev]"

# Now you can:
pytest tests/ -v              # Run tests
black sample_parse/ tests/          # Auto-format
pylint sample_parse/ tests/         # Lint
mypy sample_parse/                  # Type-check
python examples.py            # See examples
```

### Pre-Commit Hooks

Many teams automate quality checks with **git hooks**:

```bash
# Install pre-commit framework
pip install pre-commit

# Create .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.11.0
    hooks:
      - id: black
  - repo: https://github.com/PyCQA/isort
    rev: 5.12.0
    hooks:
      - id: isort
  - repo: https://github.com/PyCQA/pylint
    ...

# Install hooks
pre-commit install

# Now, on `git commit`:
# - black auto-formats
# - isort organizes imports
# - pylint checks for errors
# If any fail, commit is blocked until fixed
```

This project didn't include pre-commit for simplicity, but it's standard practice.

**Reference**: https://pre-commit.com/

### CI/CD: GitHub Actions Example

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', 3.11]
    
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install -e ".[dev]"
      - run: black --check sample_parse/ tests/
      - run: isort --check-only sample_parse/ tests/
      - run: pylint sample_parse/ tests/
      - run: mypy sample_parse/
      - run: pytest tests/ --cov=sample_parse
```

This project doesn't use GitHub Actions (to keep scope small), but professional projects do. This ensures:
- Tests pass on all supported Python versions
- Code quality standards met before merge
- Coverage doesn't regress

---

## Real-World Lessons

### 1. The Function Was Actually Simple; Testing Revealed Complexity

`parse_string_to_typed()` is ~50 lines of code. The test suite is ~270 lines.

This ratio seems wrong until you ship to production and discover:
- Users pass JSON with trailing whitespace
- Edge cases with regex metacharacters
- Different Python versions handle numbers differently
- Type consistency matters (int vs float)

Tests prevent these surprises.

### 2. Documentation As Specification

The differences between comments and docstrings matter:

```python
# Comment: explains implementation
if stripped.startswith("/") and stripped.endswith("/") and len(stripped) >= 2:

def parse_string_to_typed(value: str) -> Any:
    """Docstring: explains contract/specification
    
    Attempt to coerce a string to its most likely intended Python type...
    
    Returns:
        The parsed value in its most specific type...
    """
```

Docstrings appear in:
- IDE hover tooltips
- Generated documentation (Sphinx)
- `help(parse_string_to_typed)` in Python REPL
- API documentation websites

Comments disappear. Docstrings persist.

**Standard format**: Google-style or NumPy-style docstrings are conventional. This project uses Google-style.

**Reference**: https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings

### 3. Structure Enables Growth

A project with 200 lines can exist in a single file. But this project has:
```
sample_parse/
├── __init__.py     (public API)
├── common.py       (parsing logic)
└── cli.py          (command-line interface)
```

Why separate files?

- **Scaling**: If parsing logic grows, `common.py` contains it
- **Testing**: CLI code isn't tested directly (tested through CLI interface)
- **Reusability**: `common.py` can be used by web API and CLI alike
- **Team work**: Different people can work on `common.py` and `cli.py` without merge conflicts

The structure is *ready for growth*, not premature optimization.

### 4. Configuration Over Convention (But Convention Is Tested)

Modern Python prefers **configuration in `pyproject.toml`** over implicit behavior:

```toml
[project.scripts]
sample = "sample_parse.cli:cli"
```

This line:
- Installs a `sample` command-line tool
- Points to `sample_parse.cli` module, `cli` function
- Is discoverable by reading `pyproject.toml`

Without explicit configuration, users would need to do:
```bash
python -m sample.cli
```

Configured approach is better.

### 5. Type Hints: The ROI Improves Over Time

This project has type hints everywhere:

```python
def _regex_equals(a: Any, b: Any) -> bool:
def parse_string_to_typed(value: str) -> Any:
def test_parse(self, input_val: Any, expected: Any) -> None:
```

Costs:
- Takes time to write
- Must maintain as code evolves
- Sometimes feels verbose for simple code

Benefits:
- IDE autocomplete works perfectly
- Bugs caught at edit time, not runtime
- Code is self-documenting
- mypy finds type errors

For a learning project, the hints are pedagogical (documenting intent). For larger codebases, they're invaluable.

### 6. Linting: Diminishing Returns Are Real

This project pursues 10.00/10 pylint rating. In the real world:
- Some teams disable pylint entirely (too strict)
- Others use ruff (faster, fewer opinions)
- Many suppress specific rules (C0303, C0304 like this project does)

The lesson: **linting is a tool, not a goal**. Use it to catch real issues, not to achieve perfect scores.

--

## Tools & Resources: A Curated List

### Core Packaging
- **pip**: https://pip.pypa.io/ (package installer)
- **setuptools**: https://setuptools.pypa.io/ (build backend)
- **wheel**: https://wheel.readthedocs.io/ (binary distribution format)
- **twine**: https://twine.readthedocs.io/ (PyPI upload tool)

### Modern Alternatives to pip
- **PDM**: https://pdm-project.org/ (modern replacementfor pip-tools)
- **Poetry**: https://python-poetry.org/ (all-in-one dependency manager)
- **uv**: https://github.com/astral-sh/uv (Rust-based, fast)

### Testing
- **pytest**: https://docs.pytest.org/ (testing framework)
- **pytest-cov**: https://pytest-cov.readthedocs.io/ (coverage reports)
- **hypothesis**: https://hypothesis.readthedocs.io/ (property-based testing)

### Code Quality
- **pylint**: https://www.pylint.org/ (comprehensive linting)
- **black**: https://github.com/psf/black (code formatter)
- **isort**: https://pycqa.github.io/isort/ (import sorter)
- **mypy**: https://www.mypy-lang.org/ (static type checking)
- **ruff**: https://github.com/astral-sh/ruff (Rust-based linting, super fast)

### Type Hints & Validation
- **PEP 484**: https://www.python.org/dev/peps/pep-0484/ (type hints spec)
- **pydantic**: https://docs.pydantic.dev/ (runtime type validation)
- **typeguard**: https://typeguard.readthedocs.io/ (runtime type checking)

### Documentation
- **Sphinx**: https://www.sphinx-doc.org/ (documentation generator)
- **MkDocs**: https://www.mkdocs.org/ (markdown-based docs)
- **pdoc**: https://pdoc.dev/ (auto-generate docs from docstrings)

### CI/CD Platforms
- **GitHub Actions**: https://github.com/features/actions (built into GitHub)
- **GitLab CI**: https://docs.gitlab.com/ee/ci/ (GitLab's equivalent)
- **CircleCI**: https://circleci.com/ (cloud-native CI)

### Framework Examples
- **Django**: https://www.djangoproject.com/ (web framework; exemplary project structure)
- **FastAPI**: https://fastapi.tiangolo.com/ (modern async web framework)
- **Click**: https://click.palletsprojects.com/ (CLI framework, used here)

### Standards & PEPs
- **PEP 8**: https://www.python.org/dev/peps/pep-0008/ (style guide)
- **PEP 517/518**: https://www.python.org/dev/peps/pep-0517/ (build system)
- **PEP 621**: https://www.python.org/dev/peps/pep-0621/ (pyproject.toml spec)

---

## Summary: The Gestalt of Modern Python

If you had to distill modern Python development to essentials:

1. **Project metadata lives in `pyproject.toml`** (not setup.py, not setup.cfg)
2. **Code and tests are separate directories** (psychological and practical boundary)
3. **Tests are comprehensive, parametrized, and run automatically** (specification + regression protection)
4. **Code quality is automated** (black, isort, pylint, mypy run without human intervention)
5. **Types are optional but encouraged** (hint, don't enforce)
6. **Documentation is embedded in docstrings** (not separate files)
7. **Tools are configured in pyproject.toml** (single source of truth)
8. **Virtual environments isolate dependencies** (not Python 2's global mess)
9. **CI/CD enforces quality before merge** (gates, not suggestions)

The `sample-parse` project embodies these principles. Use it as a reference when starting new projects.

---

**Feedback welcome.** This document reflects Python culture as of 2024-2026. The ecosystem evolves; revisit these practices annually.

