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

## Secret guard exceptions

none
