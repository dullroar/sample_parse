---
gist: "Read when: considering eval, exec or any change that could execute input, or adding a new literal syntax."
---

# No code execution while parsing

**Decision.** Use `ast.literal_eval` rather than `eval` so Python-literal convenience never introduces code execution.

**Contradicted by.** Any parsing feature that would require evaluating arbitrary expressions.
