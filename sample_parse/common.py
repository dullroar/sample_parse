"""Parsing utility for smart type coercion from strings."""

import ast
import json
import re
from typing import Any


# Metacharacters that suggest something is intentionally a regex
# rather than a plain string that happens to be valid syntax.
_REGEX_METACHAR = re.compile(r"[\\^$.*+?{}\[\]|()]")


def _looks_like_regex(s: str) -> bool:
    """
    Heuristic: the string is wrapped in / / delimiters (JS/Perl style),
    OR it contains regex metacharacters and successfully compiles.
    We do NOT want plain words like 'hello' to match just because
    re.compile('hello') succeeds.
    """
    stripped = s.strip()
    if len(stripped) >= 2 and stripped.startswith("/") and stripped.endswith("/"):
        pattern = stripped[1:-1]
        try:
            re.compile(pattern)
            return True
        except re.error:
            return False
    if _REGEX_METACHAR.search(stripped):
        try:
            re.compile(stripped)
            return True
        except re.error:
            pass
    return False


def parse_string_to_typed(value: str) -> Any:  # pylint: disable=too-many-return-statements
    """
    Attempt to coerce a string to its most likely intended Python type,
    trying from most-complex to least:

        JSON object/array → Pythonic literal (dict, list, set, tuple,
        bool, int, float) → regex pattern → float → int → str (fallback)

    Args:
        value: The raw string to parse.

    Returns:
        The parsed value in its most specific type, or the original
        string if nothing else matches.
    """
    if not isinstance(value, str):
        return value  # already typed, pass through

    stripped = value.strip()

    # --- Pass 1: strict JSON (object, array, true/false/null, number) ---
    try:
        parsed = json.loads(stripped)
        # json.loads turns JSON null → None, true/false → bool, etc.
        return parsed
    except (json.JSONDecodeError, ValueError):
        pass

    # --- Pass 2: Pythonic literals via AST ---
    # Catches: dict {}, list [], tuple (), set {...} that JSON won't
    # (e.g. single-quoted strings, trailing commas, Python True/False,
    # set literals). Also catches int/float/bool/None that slipped
    # past JSON (e.g. leading-zero ints in some edge cases).
    try:
        parsed = ast.literal_eval(stripped)
        return parsed
    except (ValueError, SyntaxError):
        pass

    # --- Pass 3: regex pattern ---
    if _looks_like_regex(stripped):
        # Unwrap / / delimiters if present, return a compiled pattern.
        pattern = stripped[1:-1] if (stripped.startswith("/") and
                                     stripped.endswith("/") and
                                     len(stripped) >= 2) else stripped
        return re.compile(pattern)

    # --- Pass 4 & 5: Try numeric parsing (float, then int) ---
    # Try float first to catch '3.14', '1e10', '-0.5', etc.
    try:
        return float(stripped)
    except ValueError:
        # Try int with auto-detect of base (0x, 0o, 0b)
        try:
            return int(stripped, 0)
        except ValueError:
            pass

    # --- Fallback: it's just a string ---
    return value
