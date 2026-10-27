# EX-AMIGA API and content admin

The public API remains Flask + SQLAlchemy. A separate Django admin process edits
the existing SQLite `tour_dates` and `shoutouts` tables; it does not recreate or
migrate those content tables. Both processes use the same `EXAMIGA_DB_PATH`.
Dependencies are managed with [uv](https://docs.astral.sh/uv/).

## Install

```sh
uv sync
```

Install the optional Django admin dependency group when working on or deploying
the admin:

```sh
uv sync --group admin
```

## Run (dev)

```sh
uv run python seed.py   # add/update starter dates without deleting other records
uv run python app.py    # Flask API: http://localhost:5000
EXAMIGA_ADMIN_DEBUG=true uv run --group admin python manage.py runserver 127.0.0.1:8000
```

Open the admin at <http://localhost:8000/admin/>. Local admin mode uses an
insecure development-only key; never enable `EXAMIGA_ADMIN_DEBUG` in production.
For a fresh database, apply Django's authentication/admin tables and create a
login:

```sh
EXAMIGA_ADMIN_DEBUG=true uv run --group admin python manage.py migrate
EXAMIGA_ADMIN_DEBUG=true uv run --group admin python manage.py createsuperuser
```

## Run (prod)

```sh
uv run gunicorn --bind 127.0.0.1:5000 app:app
uv run --group admin gunicorn --bind 127.0.0.1:8000 admin_console.wsgi:application
```

The admin process requires `EXAMIGA_ADMIN_SECRET_KEY`,
`EXAMIGA_ADMIN_ALLOWED_HOSTS`, and (when served over HTTPS) an
`EXAMIGA_ADMIN_CSRF_TRUSTED_ORIGINS` value. See the repository's
[deployment guide](../DEPLOYMENT.md) before exposing it publicly. Keep the admin
behind HTTPS and do not expose port 8000 directly to the internet.
