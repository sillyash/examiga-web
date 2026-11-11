# Deployment

How EX-AMIGA runs for real, as opposed to local development (see

<web readme.md=""> and <api readme.md=""> for that).</api></web>

## Frontend: GitHub Pages

Every push to `main` that touches `web/` is built and deployed to <https://examigaband.com> by [`.github/workflows/deploy-pages.yml`](.github/workflows/deploy-pages.yml).

The builduses the `VITE_API_BASE_URL` repo variable to find the API.

## Backend: Raspberry Pi

The Django REST Framework API and content admin run in one Gunicorn service behind nginx.

The public API is at `api.examigaband.com` , route `/admin/` through a dedicated HTTPS hostname such as `admin.examigaband.com` to the same local Gunicorn port.

Do not expose Gunicorn directly to the internet. The host-specific setup (systemd unit, nginx vhosts, DNS, certs) lives in the homelab repo under `services/examiga/` and must be updated there as part of deployment.

The OpenAPI document and Swagger UI are at `/openapi.json` and `/docs/` .

The SQLite DB defaults to `api/db.sqlite3` . Set `EXAMIGA_DB_PATH` to put it somewhere else; on the Pi it's `/var/lib/examiga/db.sqlite3` , so the deployed code can stay read-only.

### Django admin configuration

Set these variables for the admin service in its systemd environment:

Variable                       | Value
:----------------------------- | :------------------------------------------
`EXAMIGA_DB_PATH`              | `/var/lib/examiga/db.sqlite3`
`EXAMIGA_SECRET_KEY`           | to a generated, persistent secret
`EXAMIGA_ALLOWED_HOSTS`        | `api.examigaband.com,admin.examigaband.com`
`EXAMIGA_CSRF_TRUSTED_ORIGINS` | `https://admin.examigaband.com`
`EXAMIGA_ADMIN_STATIC_ROOT`    | `/var/lib/examiga/staticfiles`

> [!WARNING]
>
> Keep `EXAMIGA_DEBUG` unset or `false` in production.

Configure nginx to terminate TLS, forward `Host` and `X-Forwarded-Proto` , and serve Django static files from the configured `EXAMIGA_ADMIN_STATIC_ROOT` after running `uv run python manage.py collectstatic --noinput`.

Run one Gunicorn worker to preserve the existing in-memory per-IP rate-limit behavior. Bind only to `127.0.0.1:5000` .

`migrate` creates both tables and loads the data from `api/backup/*.json` (a snapshot of the prod API), then add an admin user:

```sh
uv run python manage.py migrate
uv run python manage.py createsuperuser
```

Generate the admin secret once and store it in the service environment; do not use the local development key in production.
