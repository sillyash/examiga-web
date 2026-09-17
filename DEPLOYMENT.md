# Deployment

This covers running EX-AMIGA for real (GitHub Pages and/or a Raspberry Pi), as
opposed to local development — see [web/README.md](web/README.md) and
[api/README.md](api/README.md) for that. No Docker, just the same tools as dev
(npm, uv) run in production mode.

## Frontend

Static Vite build:

```sh
cd web
npm run build   # outputs web/dist/
```

- **GitHub Pages**: publish `web/dist/` (e.g. a `gh-pages` deploy action, or pushing
  `dist/` to a `gh-pages` branch).
- **Raspberry Pi**: serve `web/dist/` directly with nginx (see below).

## Backend (Raspberry Pi only — GitHub Pages can't run it)

```sh
cd api
uv sync
uv run gunicorn --bind 127.0.0.1:5000 app:app
```

To keep it running after you log out / across reboots, wrap it in a systemd unit,
e.g. `/etc/systemd/system/examiga-api.service`:

```ini
[Unit]
Description=EX-AMIGA API
After=network.target

[Service]
WorkingDirectory=/home/pi/examiga-web/api
ExecStart=/home/pi/.local/bin/uv run gunicorn --bind 127.0.0.1:5000 app:app
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Then `sudo systemctl enable --now examiga-api`. `api/examiga.db` lives on disk next to
the code, so it just persists across restarts — nothing extra to mount.

## nginx reverse proxy

`nginx/conf.d/` is currently empty. A minimal config to serve the static frontend and
proxy `/api/` to the gunicorn process on a Pi would look like:

```nginx
server {
    listen 80;
    server_name examiga.local;

    root /var/www/examiga/dist;   # web/dist contents
    index index.html;

    location /api/ {
        proxy_pass http://127.0.0.1:5000/api/;
    }

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

Drop that (adjusted) into `nginx/conf.d/examiga.conf` when it's time to wire this up.
