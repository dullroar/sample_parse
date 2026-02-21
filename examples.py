"""
Quick examples showcasing parse_string_to_typed functionality.

Run this script to see the module in action. Great for getting a feel
for how the parser handles different input types.

    python examples.py
"""

from sample_parse import parse_string_to_typed


def print_example(input_val, description=""):
    """Pretty-print a parsing example."""
    result = parse_string_to_typed(input_val)
    result_type = type(result).__name__

    desc_str = f" - {description}" if description else ""
    print(f"  Input:  {repr(input_val)}{desc_str}")
    print(f"  Output: {repr(result)} ({result_type})")
    print()


def show_json_examples():
    """Display JSON parsing examples."""
    print("JSON Parsing")
    print("-" * 70)
    print_example('{"name": "Alice", "age": 30}', "JSON object")
    print_example('[1, 2, 3, 4, 5]', "JSON array")
    print_example('true', "JSON boolean")
    print_example('null', "JSON null")
    print_example('3.14159', "JSON number")
    print()


def show_literals_examples():
    """Display Python literal parsing examples."""
    print("Python Literals (non-JSON)")
    print("-" * 70)
    print_example('(1, 2, 3)', "Tuple")
    print_example('{1, 2, 3}', "Set")
    print_example('True', "Python True")
    print_example('None', "Python None")
    print()


def show_regex_examples():
    """Display regex pattern parsing examples."""
    print("Regex Patterns")
    print("-" * 70)
    print_example('/[a-z]+/', "Regex with delimiters")
    print_example('^[0-9]{3}-[0-9]{4}$', "Phone number pattern")
    email_pattern = '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}'
    print_example(email_pattern, "Email pattern")
    print()


def show_number_examples():
    """Display number parsing examples."""
    print("Numbers")
    print("-" * 70)
    print_example('42', "Integer")
    print_example('-3.14', "Negative float")
    print_example('1e10', "Scientific notation")
    print_example('0xFF', "Hexadecimal")
    print_example('0b1010', "Binary")
    print_example('0o755', "Octal (permissions)")
    print()


def show_string_examples():
    """Display plain string examples."""
    print("Plain Strings (Fallback)")
    print("-" * 70)
    print_example('hello', "Simple word")
    print_example('not a number', "Phrase")
    print_example('  whitespace-preserved  ', "Whitespace-only input")
    print()


def show_passthrough_examples():
    """Display non-string passthrough examples."""
    print("Non-String Values (Pass-through)")
    print("-" * 70)
    result = parse_string_to_typed(42)
    print(f"  Input:  {42} (already a number)")
    print(f"  Output: {result} (unchanged)")
    print()

    result = parse_string_to_typed([1, 2, 3])
    print(f"  Input:  {[1, 2, 3]} (already a list)")
    print(f"  Output: {result} (unchanged)")
    print()


def show_config_example():
    """Display a real-world config parser example."""
    print("Real-World Example: Config Parser")
    print("-" * 70)
    config_entries = [
        ('timeout', '30'),
        ('max_retries', '5'),
        ('enabled', 'true'),
        ('endpoints', '["api1.example.com", "api2.example.com"]'),
        ('ignore_pattern', '/\\.tmp$/'),
    ]

    config = {}
    for key, value in config_entries:
        config[key] = parse_string_to_typed(value)
        print(f"  config[{repr(key)}] = {repr(config[key])}")

    print()


def main():
    """Run through examples of the parser's capabilities."""
    print("=" * 70)
    print("parse_string_to_typed() - Quick Examples")
    print("=" * 70)
    print()

    show_json_examples()
    show_literals_examples()
    show_regex_examples()
    show_number_examples()
    show_string_examples()
    show_passthrough_examples()
    show_config_example()

    print("=" * 70)
    print("For comprehensive tests, run: pytest tests/ -v")
    print("=" * 70)


if __name__ == "__main__":
    main()