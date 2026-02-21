"""
Comprehensive test suite for parse_string_to_typed using pytest.

Tests all parsing pathways and edge cases with parametrized test cases.
"""

import re
from typing import Any

import pytest

from sample_parse import parse_string_to_typed


# Test cases as a list of tuples: (input, expected_output)
PARSE_TEST_CASES = [
    # ===== JSON PARSING TESTS =====
    # JSON objects
    ('{"key": "value"}', {"key": "value"}),
    ('{"a": 1, "b": 2}', {"a": 1, "b": 2}),
    ('{}', {}),

    # JSON arrays
    ('[1, 2, 3]', [1, 2, 3]),
    ('[]', []),
    ('["a", "b", "c"]', ["a", "b", "c"]),

    # JSON primitives
    ('true', True),
    ('false', False),
    ('null', None),

    # JSON numbers
    ('42', 42),
    ('3.14', 3.14),
    ('-10', -10),
    ('-0.5', -0.5),
    ('1e10', 1e10),
    ('1.5e-3', 1.5e-3),

    # ===== PYTHONIC LITERAL TESTS (non-JSON) =====
    # Python True/False/None (not JSON)
    ('True', True),
    ('False', False),
    ('None', None),

    # Python tuples (not valid JSON)
    ('(1, 2, 3)', (1, 2, 3)),
    ('()', ()),
    ('("a", "b")', ("a", "b")),

    # Python sets (not valid JSON)
    ('{1, 2, 3}', {1, 2, 3}),
    ('{42}', {42}),

    # Python lists with various types
    ('[1, 2, 3]', [1, 2, 3]),

    # ===== REGEX PATTERN TESTS =====
    # Regex with / / delimiters
    ('/hello/', re.compile('hello')),
    ('/[a-z]+/', re.compile('[a-z]+')),
    ('/^test$/', re.compile('^test$')),

    # Regex with metacharacters (no delimiters)
    ('[a-z]+', re.compile('[a-z]+')),
    ('\\d{3}', re.compile('\\d{3}')),
    ('^start', re.compile('^start')),
    ('end$', re.compile('end$')),
    ('(group)', re.compile('(group)')),
    ('a|b', re.compile('a|b')),
    ('.*', re.compile('.*')),

    # ===== FLOAT PARSING TESTS =====
    ('3.14', 3.14),
    ('.5', 0.5),
    ('1e10', 1e10),
    ('1E10', 1e10),
    ('1e-10', 1e-10),
    ('-3.14', -3.14),
    ('+2.5', 2.5),
    ('0.0', 0.0),

    # ===== INTEGER PARSING TESTS =====
    # Decimal integers
    ('0', 0),
    ('42', 42),
    ('-7', -7),
    ('+10', 10),

    # Hex integers
    ('0xFF', 255),
    ('0xff', 255),
    ('0x10', 16),

    # Octal integers
    ('0o10', 8),
    ('0O77', 63),

    # Binary integers
    ('0b101', 5),
    ('0B1010', 10),

    # ===== EDGE CASES & FALLBACKS TO STRING =====
    # Whitespace handling (original strings returned if no match)
    ('  hello  ', '  hello  '),
    ('  42  ', 42),
    ('\t3.14\n', 3.14),

    # Empty and whitespace-only
    ('', ''),
    ('   ', '   '),

    # Invalid JSON/literals that should be strings
    ('not a number', 'not a number'),
    # Note: {invalid} contains {} which are regex metacharacters
    ('{invalid}', re.compile('{invalid}')),
    ('[unclosed', '[unclosed'),
    # Note: {"bad": invalid} contains {} which are regex metacharacters
    ('{"bad": invalid}', re.compile('{"bad": invalid}')),

    # Plain words (should NOT be treated as regex)
    ('hello', 'hello'),
    ('world', 'world'),
    ('foo', 'foo'),

    # Strings that happen to compile as regex but are plain text
    ('abc', 'abc'),
    ('123', 123),

    # ===== NON-STRING PASSTHROUGH =====
    # These should pass through unchanged
    (42, 42),
    (3.14, 3.14),
    (True, True),
    (None, None),
    ([1, 2, 3], [1, 2, 3]),
    ({"key": "value"}, {"key": "value"}),
]


def _regex_equals(a: Any, b: Any) -> bool:
    """Compare two values, with special handling for compiled regex patterns."""
    if isinstance(a, type(re.compile(''))) and isinstance(b, type(re.compile(''))):
        return a.pattern == b.pattern
    return a == b


class TestParseStringToTyped:
    """Test suite for parse_string_to_typed function."""

    @pytest.mark.parametrize("input_val,expected", PARSE_TEST_CASES)
    def test_parse(self, input_val: Any, expected: Any) -> None:
        """Test parsing of various input types to their intended output types.

        Args:
            input_val: The input value to parse.
            expected: The expected output value.
        """
        result = parse_string_to_typed(input_val)
        assert _regex_equals(result, expected), (
            f"Input: {repr(input_val)}\n"
            f"Expected: {repr(expected)} (type: {type(expected).__name__})\n"
            f"Got: {repr(result)} (type: {type(result).__name__})"
        )


class TestJsonParsing:
    """Integration tests for JSON parsing."""

    def test_json_object(self) -> None:
        """JSON objects should be parsed to dicts."""
        assert parse_string_to_typed('{"key": "value"}') == {"key": "value"}

    def test_json_array(self) -> None:
        """JSON arrays should be parsed to lists."""
        assert parse_string_to_typed('[1, 2, 3]') == [1, 2, 3]

    def test_json_primitives(self) -> None:
        """JSON primitives should be parsed correctly."""
        assert parse_string_to_typed('true') is True
        assert parse_string_to_typed('false') is False
        assert parse_string_to_typed('null') is None


class TestRegexParsing:
    """Integration tests for regex pattern parsing."""

    def test_slash_delimited_regex(self) -> None:
        """Regex patterns with / / delimiters should be compiled."""
        result = parse_string_to_typed('/[a-z]+/')
        assert isinstance(result, type(re.compile('')))
        assert result.pattern == '[a-z]+'

    def test_metacharacter_regex(self) -> None:
        """Strings with regex metacharacters should be compiled."""
        result = parse_string_to_typed('[a-z]+')
        assert isinstance(result, type(re.compile('')))
        assert result.pattern == '[a-z]+'

    def test_plain_word_not_regex(self) -> None:
        """Plain words without metacharacters should remain strings."""
        assert parse_string_to_typed('hello') == 'hello'
        assert parse_string_to_typed('world') == 'world'


class TestNumberParsing:
    """Integration tests for number parsing."""

    def test_float_parsing(self) -> None:
        """Decimal numbers should be parsed as floats."""
        assert parse_string_to_typed('3.14') == 3.14
        assert parse_string_to_typed('.5') == 0.5
        assert parse_string_to_typed('1e10') == 1e10

    def test_integer_parsing(self) -> None:
        """Integers in various bases should be parsed correctly."""
        assert parse_string_to_typed('42') == 42
        assert parse_string_to_typed('0xFF') == 255
        assert parse_string_to_typed('0o10') == 8
        assert parse_string_to_typed('0b101') == 5

    def test_negative_numbers(self) -> None:
        """Negative numbers should be parsed correctly."""
        assert parse_string_to_typed('-7') == -7
        assert parse_string_to_typed('-3.14') == -3.14


class TestEdgeCases:
    """Integration tests for edge cases and fallbacks."""

    def test_empty_string(self) -> None:
        """Empty strings should be returned as-is."""
        assert parse_string_to_typed('') == ''

    def test_whitespace_only(self) -> None:
        """Whitespace-only strings should be returned as-is."""
        assert parse_string_to_typed('   ') == '   '

    def test_invalid_json_fallback(self) -> None:
        """Invalid JSON should fall back to string or regex."""
        assert parse_string_to_typed('not a number') == 'not a number'
        assert parse_string_to_typed('[unclosed') == '[unclosed'

    def test_passthrough_non_strings(self) -> None:
        """Non-string values should pass through unchanged."""
        assert parse_string_to_typed(42) == 42
        assert parse_string_to_typed(3.14) == 3.14
        assert parse_string_to_typed([1, 2, 3]) == [1, 2, 3]
        assert parse_string_to_typed({"key": "value"}) == {"key": "value"}


class TestPythonLiterals:
    """Integration tests for Python-specific literals."""

    def test_python_booleans_and_none(self) -> None:
        """Python keywords should be parsed correctly."""
        assert parse_string_to_typed('True') is True
        assert parse_string_to_typed('False') is False
        assert parse_string_to_typed('None') is None

    def test_python_tuples(self) -> None:
        """Tuples (non-JSON) should be parsed."""
        assert parse_string_to_typed('(1, 2, 3)') == (1, 2, 3)
        assert parse_string_to_typed('()') == ()

    def test_python_sets(self) -> None:
        """Sets (non-JSON) should be parsed."""
        assert parse_string_to_typed('{1, 2, 3}') == {1, 2, 3}
        assert parse_string_to_typed('{42}') == {42}