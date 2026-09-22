# DESIGN.md

# sample-parse Design

## Boundary

sample-parse is a small utility that coerces a string into the most plausible Python value. README.md documents installation and use; the ordered parsing policy lives in `sample_parse/common.py`.

## Core decisions

- Parse in a deliberate specificity order: strict JSON, safe Python literals through `ast.literal_eval`, intentional-looking regular expressions, numeric values, then the original string.
- Use `ast.literal_eval` rather than `eval` so Python-literal convenience does not introduce code execution.
- Compile a regex only when delimiters or metacharacters suggest intent; ordinary words should remain strings even though they are valid regexes.
- Keep the Click CLI as a thin wrapper over the same parsing function used by library callers.

## Constraints

The parser is heuristic, not a schema validator. Ambiguous values are resolved by the documented order, so callers requiring an exact type should validate after parsing or supply a schema.


