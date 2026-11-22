# Agent contract

sample_parse is a Python library and Click CLI. It converts a string to the most plausible Python value. The order of the conversions is in `sample_parse/common.py`.

## Standing rules

- Before changing this repository's structure, read [repo-template](https://github.com/dullroar/repo-template) and [ralph-looper](https://github.com/dullroar/ralph-looper). Account for their layout, plan format, generated indexes, worktree rules, and validation commands in the change.
- Start work on a branch. Use a separate Git worktree for each plan and for steps that run at the same time. Keep `master` available for review.
- Use placeholders and aggregate evidence. Keep secrets, credentials, personal data, personal paths, private host names, and sensitive record-level examples out of tracked files. Keep logs and other run output outside the repository.
- Write in Simplified Technical English. Use short sentences, active voice, and consistent terms.
- Get authorization before you push, publish, force-push, or add a remote.

User instructions come first. When sources conflict, use this order after user instructions: this file, `docs/design/`, the named plan, other docs and references, `memory/`, code and tests, historical notes.

## Load context in this order

1. Read this file and [README.md](./README.md).
2. Read the [docs index](./docs/README.md), [memory index](./memory/AGENTS.md), [plans index](./plans/AGENTS.md), and [scripts index](./scripts/AGENTS.md).
3. Open only the documents or scripts whose routing entries match the task. For a large file, search its headings and read the relevant sections.
4. Stop when you know the decision, the files, the limits, and how to verify the work.

## Context ownership

| Path | What belongs here |
| --- | --- |
| `AGENTS.md` | Rules that apply to the entire repository. |
| `docs/design/` | Design reasons, with one premise in each file. |
| `memory/` | Findings that cost time to discover, with one topic in each file. Edit the existing topic when it changes. |
| `plans/` | Requirements, steps, and execution state. |
| `scripts/` | Deterministic automation. |

Keep each fact in its source file. Start each routed Markdown file with `gist: "Read when: ..."` or `gist: "Read me when: ..."` in its front matter. Edit the docs index by hand. Run `python3 scripts/build_indexes.py` to update generated index blocks.

## Planned work

- Work on a named plan in `plans/<plan>/` or on an explicitly identified off-plan task. Copy [plans/for-each-plan/](./plans/for-each-plan/) to start a plan.
- After the spec is approved, carry out the steps. Diagnose test failures within scope and continue. Return to the user for a decision when requirements conflict, scope must expand, or an action exceeds the authority in the spec.
- Preserve every acceptance check named in the spec. If a protected check cannot pass as written, escalate.
- Run steps at the same time only when they are independent and their `touches` do not overlap. If independence is uncertain, run them in order. Run the spec's combined validation after the steps merge.
- Record the evidence in the step file before you mark it done. Report unavailable verification. Record what remains in Resume notes if you stop before completion.
- Record whether a change retires a rule, corrects documentation, or accepts a known violation. See the [spec template](./plans/for-each-plan/spec.md).

## Validation

Run the smallest check that proves the change. For changes to context files, run `python3 scripts/check_context.py`.
