---
gist: "Read when: changing the parse order, adding a recognized value type, or deciding how an ambiguous string should resolve."
---

# Ordered specificity parsing

**Decision.** Parse in a deliberate order: strict JSON, safe Python literals through `ast.literal_eval`, intentional-looking regular expressions, numeric values, then the original string. A regex is compiled only when delimiters or metacharacters suggest intent, so ordinary words stay strings.

**Boundary.** The parser is heuristic, not a schema validator. Callers needing an exact type should validate after parsing or supply a schema.
