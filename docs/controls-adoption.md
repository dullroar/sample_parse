---
gist: "Read me when: you run, debug or change the pinned deterministic-controls library, the check_context.py shim or the Docker cache for the shim."
---

# Controls adoption

This repository runs the pinned `deterministic-controls` library in advisory mode. The `controls` CI job is not a required check yet.

## How it works

- `scripts/check_context.py` is a shim. It runs the library from a cached virtual environment.
- `scripts/controls-requirements.txt` holds the pin: one install line with a full commit. The shim reads it.
- `controls.toml` lists the enabled checks and the profile.
- The cache path is `$XDG_CACHE_HOME/deterministic-controls/<commit>/` (default `~/.cache/deterministic-controls/<commit>/`).
- The first run for a commit needs the network. The shim builds the cache then. Later runs need no network.
- The shim keeps the old output lines (`ok  <script>` or `FAIL <script>`) and the exit codes `0` and `1`.
- The shim exits `2` if the library cannot run. It never passes without a result. It never falls back to the old scripts.
- The old check scripts stay in `scripts/`. They are not used by the shim.

## How the adoption was made

1. Audit (step `a01-audit`): a read-only audit. The result is in `docs/controls-audit.json`.
2. Plan: `adopt plan` with the pinned commit, as a dry run. A person read the diff.
3. Apply: `adopt apply` with the same commit, on a clean tree. Then the step added the Docker cache, the `AGENTS.md` rule and this file.

## Where the tools did not fit

- **Docker run has no network.** The container runs with `--network none --read-only`. The shim cannot build its cache there. The `Dockerfile` now builds the cache at image build time, as user `tester`, because the cache is under that user's home. The build has network access.
- **The image needs `git`.** The shim setup installs the library from a Git URL. `tests/test_secret_guard.py` also needs `git`. The `Dockerfile` installs it with `apt-get` as root.
- **`adopt apply` wrote a file outside the step scope.** It changed `scripts/install_hooks.sh` (a `secretguard.path` fallback). The step reverted that file. A later step or the operator may take that change on purpose.
- **The generated `controls` job lacked `persist-credentials: false`.** The step added it, to match the `check` job.
- **The generated `controls` job repeats the guard steps of the `check` job.** This is accepted.
- **Run-time writes.** The shim writes nothing outside `/tmp` in the Docker run when the cache is complete. Check this in the Docker gate. The session that wrote this text could not run Docker.

## Probes

Run date (UTC): 2026-11-24.

Each probe ran in a throwaway clone under `.probe/` inside the worktree. The command was `python3 -m deterministic_controls check --root <copy> --profile ci --format json`. The rule ID comes from the JSON. The real tree was not changed. The probe clones were deleted before the gate.

| Probe | Expected check | Rule ID in the result | Exit code | Result |
| --- | --- | --- | --- | --- |
| Broken relative link in a Markdown file | `markdown.local-links` | `markdown.local-links.missing-file` | 1 | Failed as expected. |
| Stale generated index (a script header changed, index not rebuilt) | `context.index-freshness` | `context.index-freshness.stale` | 1 | Failed as expected. |
| Plan step without `gate` | `plans.schema` | `plans.schema.missing-gate` | 1 | Failed as expected. |
| Synthetic token in a Markdown file (built at run time, committed in the copy only) | `security.secrets` | `security.secrets.github-token` | 1 | Failed as expected. `security.personal-data` also reported it. |
| Tracked `driver.out` file | `repo.forbidden-artifacts` | `repo.forbidden-artifacts.tracked` | 1 | Failed as expected. |
| Internal error (a tracked file made unreadable) | none (the check must not pass) | none (check status `error`, `PermissionError`) | 3 | Did not pass, as expected. |
| Clean clone of `HEAD` | none | none | 0 | Passed. |
| Copy of the unreadable-file probe after the file mode was restored | none | none | 0 | Passed. |
| Shim `python3 scripts/check_context.py` in the copy with the plan step without `gate` | `plans.schema` | `FAIL check_plan.py` in the shim output | 1 | Failed as expected. |

The synthetic token is not written in any tracked file. The secret guard has no exceptions.

## Rollback

Run date (UTC): 2026-11-24.

Test result:

- The base commit is the parent of the `adopt apply` commit. A clean clone at that commit ran its own `python3 scripts/check_context.py` (the old scripts). Exit code `0`. All four old scripts printed `ok`.
- A clean clone of `HEAD` ran the new shim `python3 scripts/check_context.py`. Exit code `0`. All lines printed `ok`.
- Both pass. This shows that the old checks still work on the pre-adoption tree and the shim works on the adopted tree.

Files of the adoption commit (`adopt apply` and the step that finished it):

- Added: `controls.toml`, `scripts/controls-requirements.txt`, `docs/controls-adoption.md`.
- Changed: `scripts/check_context.py` (now a shim), `.github/workflows/context.yml` (new `controls` job), `Dockerfile` (git and the cache), `AGENTS.md` (one rule), `docs/README.md` and `scripts/AGENTS.md` (index entries).
- Kept: the old check scripts in `scripts/`, `scripts/test_docker.sh`, the `check` CI job, the tests and the product code.

Steps to roll back:

1. Option A, change the pin: edit `scripts/controls-requirements.txt`. Put the previous commit in the install line. There is no earlier pin today, so use option B for a full rollback.
2. Option B, revert: create a new branch. Run `git revert` on the adoption commits. Or restore the changed files from the base commit with `git checkout <base> -- <file>` and delete the added files.
3. Run `python3 scripts/check_context.py`. It must exit `0`.

The cache under `$XDG_CACHE_HOME/deterministic-controls/<commit>/` is safe to delete. The shim builds it again on the next run (this needs the network).

## Receipt

Run date (UTC): 2026-11-24.

The command was `python3 -m deterministic_controls adopt receipt --root <clean clone> --commit 3a2e9f3d95136958c54f73c831e84b971fc9a054`. It ran in a clean clone of `HEAD`.

Notes:

- `repository` is the name of the temporary clone, not the name of this repository.
- `files_added` and `files_changed` are empty in a clean clone. This is a known library defect. The files of the adoption are listed in the Rollback section.
- `enforcement_state` is `advisory`.
- `base_revision` is the `HEAD` of the clone, not the commit before the adoption.

```json
{
  "base_revision": "b16d9baf210a9751ad31b6d905792d969af12d28",
  "checks_run": [
    {
      "check_id": "context.index-freshness",
      "status": "passed"
    },
    {
      "check_id": "markdown.local-links",
      "status": "passed"
    },
    {
      "check_id": "plans.graph",
      "status": "passed"
    },
    {
      "check_id": "plans.schema",
      "status": "passed"
    },
    {
      "check_id": "repo.forbidden-artifacts",
      "status": "passed"
    },
    {
      "check_id": "security.personal-data",
      "status": "passed"
    },
    {
      "check_id": "security.secrets",
      "status": "passed"
    }
  ],
  "commands_kept": [
    "scripts/build_context_indexes.py",
    "scripts/build_indexes.py",
    "scripts/check_links.py",
    "scripts/check_plan.py",
    "scripts/ctx_common.py",
    "scripts/scan_context_secrets.py",
    "scripts/scan_secrets.py",
    "scripts/test_docker.sh",
    "test: python3 -m unittest discover -s tests",
    "test: docker build (Dockerfile)",
    "ci-job: check"
  ],
  "control_pin": "3a2e9f3d95136958c54f73c831e84b971fc9a054",
  "date": "2026-11-24",
  "enabled_checks": [
    "context.index-freshness",
    "markdown.local-links",
    "plans.graph",
    "plans.schema",
    "repo.forbidden-artifacts",
    "security.personal-data",
    "security.secrets"
  ],
  "enforcement_state": "advisory",
  "files_added": [],
  "files_changed": [],
  "profile": "ci",
  "repository": "head",
  "rollback": [
    "To restore the previous pin: edit scripts/controls-requirements.txt, put the previous commit in the install line, and run scripts/check_context.py once to build its environment.",
    "To remove the adoption: run 'git revert' on the adoption commit, or restore these files from the base revision b16d9baf210a9751ad31b6d905792d969af12d28 with 'git checkout b16d9baf210a9751ad31b6d905792d969af12d28 -- <file>' and delete the files that were added: scripts/check_context.py, scripts/controls-requirements.txt, controls.toml, scripts/secret_guard.py, scripts/install_hooks.sh, .github/workflows/context.yml.",
    "The cached environment is in the user cache directory under deterministic-controls/<commit>/. It is safe to delete."
  ],
  "schema_version": 1
}
```

## Secret guard exceptions

none
