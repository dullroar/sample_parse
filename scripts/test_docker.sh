#!/usr/bin/env bash
# Run me when: you want to build the Docker image and run the project and context tests.
set -euo pipefail

cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.."
work_dir=$(mktemp -d "${TMPDIR:-/tmp}/sample-parse-docker.XXXXXXXX")
run_name="sample-parse-docker-${work_dir##*.}"
image="sample-parse:${run_name,,}"

cleanup() {
    docker image rm "$image" >/dev/null 2>&1 || true
    rm -rf -- "$work_dir"
}
trap cleanup EXIT

# Copy the current contents of tracked files. Omit the linked worktree's Git pointer.
mkdir "$work_dir/source"
git ls-files --cached --deduplicate -z \
    | tar --create --file=- --no-recursion --null --files-from=- \
    | tar --extract --file=- --directory="$work_dir/source"

docker build --tag "$image" "$work_dir/source"
docker run --rm --name "$run_name" --network none --read-only \
    --tmpfs /tmp:rw,nosuid,nodev "$image"
