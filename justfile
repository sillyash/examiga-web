# EX-AMIGA dev commands. Run `just` to list them.

[private]
default:
    @just --list --unsorted

# --- setup ---

# install web + api dependencies
install:
    cd web && npm install
    cd api && uv sync --group admin

# --- dev ---

# run api + web together (Ctrl-C stops both)
dev:
    #!/usr/bin/env bash
    trap 'kill 0' EXIT
    just api & just web & wait

# vite dev server on :5173
web:
    cd web && npm run dev

# Flask API debug server on :5000
api:
    cd api && uv run python app.py

# Django admin on :8000 (local development)
admin:
    cd api && EXAMIGA_ADMIN_DEBUG=true uv run --group admin python manage.py runserver 127.0.0.1:8000

# apply Django auth/admin tables to the shared SQLite database
admin-migrate:
    cd api && EXAMIGA_ADMIN_DEBUG=true uv run --group admin python manage.py migrate

# create an admin login
admin-user:
    cd api && EXAMIGA_ADMIN_DEBUG=true uv run --group admin python manage.py createsuperuser

# add or update starter dates without deleting other dates or shoutouts
seed:
    cd api && uv run python seed.py

# delete local SQLite data only after explicit confirmation; never use a custom DB path
reset-db:
    #!/usr/bin/env bash
    set -euo pipefail
    if [[ -n "${EXAMIGA_DB_PATH:-}" ]]; then
        echo "Refusing reset while EXAMIGA_DB_PATH is set; unset it to target the local dev database." >&2
        exit 1
    fi
    if [[ "${RESET_DB_CONFIRM:-}" != "DELETE_ALL_LOCAL_DATA" ]]; then
        echo "Set RESET_DB_CONFIRM=DELETE_ALL_LOCAL_DATA to confirm deleting local tour dates and shoutouts." >&2
        exit 1
    fi
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

# run the Flask API like in production (gunicorn)
serve:
    cd api && uv run gunicorn --bind 127.0.0.1:5000 app:app

# run the Django admin like production (gunicorn; configure secrets and hosts first)
admin-serve:
    cd api && uv run --group admin gunicorn --bind 127.0.0.1:8000 admin_console.wsgi:application

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
