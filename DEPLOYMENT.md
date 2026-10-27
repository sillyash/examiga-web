# Deployment

How EX-AMIGA runs for real, as opposed to local development (see
[web/README.md](web/README.md) and [api/README.md](api/README.md) for that).

## Frontend: GitHub Pages

Every push to `main` that touches `web/` is built and deployed to
<https://examigaband.com> by
[`.github/workflows/deploy-pages.yml`](.github/workflows/deploy-pages.yml). The build
uses the `VITE_API_BASE_URL` repo variable (`https://api.examigaband.com`) to find
the API.

## Backend: Raspberry Pi

The Flask API runs behind nginx at `api.examigaband.com`. The Django content admin
is a separate Gunicorn process using the same SQLite file; route it through nginx
on a dedicated HTTPS hostname such as `admin.examigaband.com`. Do not expose its
Gunicorn port directly to the internet. The host-specific setup (systemd units,
nginx vhosts, DNS, certs) lives in the homelab repo under `services/examiga/` and
must be updated there as part of deployment.

The SQLite DB defaults to `api/examiga.db`. Set `EXAMIGA_DB_PATH` to put it somewhere
else; on the Pi it's `/var/lib/examiga/examiga.db`, so the deployed code can stay
read-only.

### Django admin configuration

Set these variables for the admin service in its systemd environment:

- `EXAMIGA_DB_PATH=/var/lib/examiga/examiga.db`
- `EXAMIGA_ADMIN_SECRET_KEY` to a generated, persistent secret
- `EXAMIGA_ADMIN_ALLOWED_HOSTS=admin.examigaband.com`
- `EXAMIGA_ADMIN_CSRF_TRUSTED_ORIGINS=https://admin.examigaband.com`
- `EXAMIGA_ADMIN_STATIC_ROOT=/var/lib/examiga/staticfiles`

Keep `EXAMIGA_ADMIN_DEBUG` unset or `false` in production. Configure nginx to
terminate TLS, forward `Host` and `X-Forwarded-Proto`, and serve Django static
files from the configured `EXAMIGA_ADMIN_STATIC_ROOT` after running
`uv run --group admin python manage.py collectstatic --noinput`. The Django process should
bind only to `127.0.0.1:8000`.

Before enabling the admin, make a SQLite backup and verify it can be restored to
a separate file. Apply Django's own auth/admin tables to the shared database and
create an admin user:

```sh
uv run --group admin python manage.py migrate
uv run --group admin python manage.py createsuperuser
```

Generate the admin secret once and store it in the service environment; do not
use the local development key in production.

The unmanaged content models do not create or alter `tour_dates` or `shoutouts`.
New fan shoutouts remain immediately visible; admin users can edit or delete
them. Keep the old Flask service and database backup available until the admin
and public API have both been smoke-tested. `just reset-db` requires an explicit
local-data confirmation and refuses to run when `EXAMIGA_DB_PATH` is set. The
seed script also refuses writes to a configured database unless explicitly
enabled.
