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

The Flask API runs on a Pi with `uv run gunicorn` behind nginx, at
`api.examigaband.com`. The host-specific setup (systemd unit, nginx vhost, DNS,
certs) lives in the [homelab repo](https://github.com/sillyash/homelab), under
`services/examiga/`.
