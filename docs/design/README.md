---
gist: "Read when: changing the repository's design, boundaries or dependencies, or before simplifying a deliberate seam."
---

# Architecture premises

One durable design decision per file: the constraint, the choice, why, and what would contradict it. Open only the premise whose **Read when** line matches the task.

<!-- BEGIN GENERATED CONTEXT INDEX -->

* [no-eval-safety-boundary.md](./no-eval-safety-boundary.md).
  Read when: considering eval, exec or any change that could execute input, or adding a new literal syntax.
* [ordered-specificity-parsing.md](./ordered-specificity-parsing.md).
  Read when: changing the parse order, adding a recognized value type, or deciding how an ambiguous string should resolve.
* [thin-cli-over-library.md](./thin-cli-over-library.md).
  Read when: adding CLI options or behavior that could diverge from the library's parsing function.

<!-- END GENERATED CONTEXT INDEX -->
