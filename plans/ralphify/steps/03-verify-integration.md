---
id: 03-verify-integration
status: done
depends_on: [02-build-and-test]
touches:
  - plans/ralphify/steps/03-verify-integration.md
lane: none
requirements: [R3]
gate: python3 scripts/check_context.py && bash scripts/test_docker.sh && git diff --check
evidence: gate passed 2026-11-22 (driver-verified)
claimed_by: codex cli-default
claimed_at: "2026-11-22T22:08:38Z"
---

# 03-verify-integration

Depends on `02-build-and-test`. Update only the step file. Rerun the context and Docker gate from the integrated worktree as the driver would. Check the template and runner links in `AGENTS.md` and the structural-change rule. Verify README commands and the existing entry points. Record the worktree base commit, exact commands, build result, test counts or concrete smoke assertions, expected opt-in skips, real FUSE result where required, and UTC date. Keep logs outside Git. Gate: `python3 scripts/check_context.py && bash scripts/test_docker.sh && git diff --check`.

The driver writes its own `evidence` field. Put detailed test evidence in the body of the verification step and commit it. The parent verifies the final child commit and result. A green build alone cannot satisfy R2 or R3.

## Repository gate

Install the existing `.[dev]` extra and run `python -m pytest tests/` in Docker. Preserve `LEARNTHIS.md`, packaging, and the example entry point. Keep Docker-only adjustments to test and packaging support.

Run `git merge-base HEAD plan/ralphify` to identify the integrated base commit. Replace each pending value in the results below. For each passing check, put details after `PASS`. Include the actual Docker commands or image reference and test counts or concrete smoke results. Record `n/a` in the FUSE field for other repos. If a required test fails or skips, record that in resume notes and leave the result pending.

## Results

- Base commit: `f22f44b04a7c63b370b8b2cf8b40cd583b3b6cc8` from
  `git merge-base HEAD plan/ralphify`.
- Commands: PASS. `python3 scripts/check_context.py && bash scripts/test_docker.sh && git diff --check`.
  The host and container context checks passed. The Docker socket required
  execution outside the sandbox.
- Docker build: PASS. The gate built
  `sample-parse:sample-parse-docker-uqjmx2ny` from the integrated worktree.
  The README build from `git archive HEAD` and the documented Docker run also
  passed with `sample-parse:manual-1795385266-40524`.
- Tests: PASS. The gate and README Docker run each passed all 89 tests on
  Python 3.12.3. The image installed the `dev` extra. From `/tmp` in the
  image, the installed CLI returned `int: 123`, JSON `123`, `float: 3.14`,
  and `Pattern: /[a-z]+/` for the README inputs. Batch JSON returned the
  values `123` and `3.14` in order. The installed library parsed `[1, 2]`
  as a list. `python examples.py` produced output on the host and in the
  image. The image included `LEARNTHIS.md`.
- Skips: PASS. Zero tests skipped. This repository has no required opt-in
  tests.
- FUSE: n/a.
- UTC date: 2026-11-22.

## README and repository checks

- PASS. Both upstream links in `AGENTS.md` resolve. The structural-change
  rule requires both references and covers layout, plan format, generated
  indexes, worktree rules, and validation commands. The pinned runner
  guide in the docs index resolves.
- PASS. The local runner help and argument parser accept
  `ralph-looper --repo . --plan ralphify --agent codex`. This verification
  checked the command syntax. The parent driver owns execution of the plan.
- PASS. `git diff --exit-code 125f194 HEAD -- LEARNTHIS.md pyproject.toml examples.py sample_parse tests`
  confirmed that the migration preserved these files.
- Known host installation issue. In a temporary archive, the README's
  editable install targets `.` and `.[dev]` both failed with
  `error: package directory './sample' does not exist`. The check used
  `pip install --no-index --no-build-isolation --no-deps -e` with each
  target. The existing package table names `sample`. The Docker build
  corrects the name in its temporary install copy. A host packaging fix
  requires a separate change.
