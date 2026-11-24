FROM ubuntu:24.04

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends ca-certificates git python3-venv \
    && rm -rf /var/lib/apt/lists/* \
    && python3 -m venv /opt/venv \
    && useradd --create-home tester

ENV PATH="/opt/venv/bin:${PATH}" \
    PYTHONDONTWRITEBYTECODE=1

# The package table still names the old directory. Fix only the install copy.
COPY pyproject.toml README.md /tmp/sample-parse-install/
COPY sample_parse/ /tmp/sample-parse-install/sample_parse/
RUN sed -i 's/^packages = \["sample"\]$/packages = ["sample_parse"]/' /tmp/sample-parse-install/pyproject.toml \
    && PIP_CONFIG_FILE=/dev/null python -m pip --no-cache-dir install '/tmp/sample-parse-install[dev]' \
    && rm -rf /tmp/sample-parse-install

WORKDIR /work
COPY . .
USER tester
# The run has no network and a read-only file system. Build the shim cache now, as user tester.
RUN python -c "import sys; sys.path.insert(0, 'scripts'); import check_context as c; spec, commit = c.pinned(); c.ensure_environment(spec, commit)"
CMD ["sh", "-eu", "-c", "output=$(mktemp -d /tmp/sample-parse.XXXXXXXX); \
    trap 'rm -rf \"$output\"' EXIT; \
    python -m pytest tests/ --basetemp=\"$output/tests\" -o cache_dir=\"$output/cache\"; \
    python scripts/check_context.py"]
