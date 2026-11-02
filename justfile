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

# Django API and admin development server on :5000
api:
    cd api && EXAMIGA_DEBUG=true uv run python manage.py runserver 127.0.0.1:5000

# create tables and load api/backup/*.json
migrate:
    cd api && EXAMIGA_DEBUG=true uv run python manage.py migrate

# create an admin login
superuser:
    cd api && EXAMIGA_DEBUG=true uv run python manage.py createsuperuser

# delete the local SQLite DB and rebuild it from migrations
reset-db:
    rm -f api/db.sqlite3
    just migrate

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

# run the Django API and admin like in production (gunicorn)
serve:
    cd api && uv run gunicorn --workers 1 --bind 127.0.0.1:5000 config.wsgi

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
