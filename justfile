# EX-AMIGA dev commands. Run `just` to list them.

[private]
default:
    @just --list --unsorted

# --- setup ---

# install web + api dependencies
install:
    cd web && npm install
    cd api && uv sync

# --- dev ---

# run api + web together (Ctrl-C stops both)
dev:
    #!/usr/bin/env bash
    trap 'kill 0' EXIT
    just api & just web & wait

# vite dev server on :5173
web:
    cd web && npm run dev

# flask debug server on :5000
api:
    cd api && uv run python app.py

# (re)seed the database
seed:
    cd api && uv run python seed.py

# delete the sqlite db and reseed from scratch
reset-db:
    rm -f api/examiga.db
    just seed

# --- quality ---

# oxlint + eslint --fix
lint:
    cd web && npm run lint

# prettier
fmt:
    cd web && npm run format

# type-check + lint (what to run before committing)
check:
    cd web && npm run type-check
    just lint

# --- build / release ---

# production build of the frontend -> web/dist
build:
    cd web && npm run build

# preview the production build
preview: build
    cd web && npm run preview

# run the api like in production (gunicorn)
serve:
    cd api && uv run gunicorn --bind 127.0.0.1:5000 app:app

# render docs/RAPPORT.md -> docs/rapport.pdf
pdf:
    scripts/md_to_pdf.sh

# build the graded submission archive (merienne_ashley_vuejs.tar.gz)
release: pdf
    scripts/package.sh

# --- versioning ---

# show current versions
version:
    @echo "web $(cd web && npm pkg get version | tr -d '\"')  api $(cd api && uv version --short --color never)"

# bump web + api to the same version (part = major|minor|patch), commit and tag
bump part="patch":
    #!/usr/bin/env bash
    set -euo pipefail
    test -z "$(git status --porcelain)" || { echo "working tree not clean" >&2; exit 1; }
    v=$(cd api && uv version --bump {{part}} --short)
    (cd web && npm version "$v" --no-git-tag-version --allow-same-version >/dev/null)
    git add api/pyproject.toml api/uv.lock web/package.json web/package-lock.json
    git commit -m "Bump version to $v"
    git tag "v$v"
    echo "bumped to v$v (not pushed: git push --follow-tags)"

# remove build outputs and caches
clean:
    rm -rf web/dist merienne_ashley_vuejs.tar.gz
    find api -name __pycache__ -type d -exec rm -rf {} +
