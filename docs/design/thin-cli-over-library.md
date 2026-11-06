---
gist: "Read when: adding CLI options or behavior that could diverge from the library's parsing function."
---

# CLI is a thin wrapper

**Decision.** The Click CLI is a thin wrapper over the same parsing function used by library callers, so the two cannot disagree about results.
