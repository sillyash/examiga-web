# EX-AMIGA API

Django + DRF + drf-spectacular, SQLite. Two tables (`TourDate`, `Shoutout`) whose schema **and data** come from migrations: `shows/migrations/0002_backup_data.py` loads `backup/*.json` (a snapshot of the prod API).

```sh
uv sync
EXAMIGA_DEBUG=true uv run python manage.py migrate
EXAMIGA_DEBUG=true uv run python manage.py createsuperuser
EXAMIGA_DEBUG=true uv run python manage.py runserver 127.0.0.1:5000
```

- `GET /api/tour-dates`, `GET|POST /api/shoutouts` (cursor-paginated, `website` honeypot, 3/min + 20/day per IP)
- `/docs/` Swagger, `/openapi.json` schema, `/admin/` admin

Prod: `uv run gunicorn --workers 1 --bind 127.0.0.1:5000 config.wsgi` with `EXAMIGA_SECRET_KEY`, `EXAMIGA_ALLOWED_HOSTS`, `EXAMIGA_CSRF_TRUSTED_ORIGINS`, optional `EXAMIGA_DB_PATH`. Keep 1 worker: rate limits live in process memory.
