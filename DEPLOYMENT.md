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

- **GitHub Pages** (production, <https://examigaband.com>): automatic, see below.
- **Raspberry Pi**: serve `web/dist/` directly with nginx (see below).

### GitHub Pages

`.github/workflows/deploy-pages.yml` builds `web/` and deploys `web/dist/` on every
push to `main` that touches `web/` (or manually via *Actions → Deploy to GitHub Pages
→ Run workflow*). The router uses hash history, so no `404.html` SPA fallback is
needed, and Vite's `base` stays `/` because the site lives at the domain root.

One-time repo setup (Settings on GitHub):

1. **Pages → Build and deployment → Source**: *GitHub Actions*.
2. **Pages → Custom domain**: `examigaband.com`, then tick **Enforce HTTPS** once
   the certificate is issued (can take up to ~1 h after DNS resolves).
   `web/public/CNAME` holds the same domain, but with Actions deploys the setting
   above is what actually counts.
3. **Secrets and variables → Actions → Variables**: add `VITE_API_BASE_URL` =
   `https://api.examigaband.com` (the API on the Pi, see below). Without it the
   site builds fine, but shows/guestbook requests hit `/api/...` on Pages and 404.
4. Optional but recommended: verify the domain under your GitHub **account**
   Settings → Pages → *Add a domain* (adds a `_github-pages-challenge-sillyash` TXT
   record), so nobody else can claim it for their Pages site.

### Cloudflare DNS for examigaband.com

In the Cloudflare dashboard → `examigaband.com` → **DNS → Records**:

| Type  | Name  | Content               | Proxy        |
|-------|-------|-----------------------|--------------|
| A     | `@`   | `185.199.108.153`     | DNS only     |
| A     | `@`   | `185.199.109.153`     | DNS only     |
| A     | `@`   | `185.199.110.153`     | DNS only     |
| A     | `@`   | `185.199.111.153`     | DNS only     |
| AAAA  | `@`   | `2606:50c0:8000::153` | DNS only     |
| AAAA  | `@`   | `2606:50c0:8001::153` | DNS only     |
| AAAA  | `@`   | `2606:50c0:8002::153` | DNS only     |
| AAAA  | `@`   | `2606:50c0:8003::153` | DNS only     |
| CNAME | `www` | `sillyash.github.io`  | DNS only     |

GitHub redirects `www.examigaband.com` → `examigaband.com` automatically.

**Keep these grey-cloud (DNS only) at least until GitHub has issued the HTTPS
certificate** — GitHub's Let's Encrypt check fails behind Cloudflare's proxy. If you
want the orange cloud (Cloudflare CDN) afterwards, first set **SSL/TLS → Overview**
to **Full (strict)**: *Flexible* makes Cloudflare talk HTTP to GitHub, which
redirects to HTTPS, and you get an infinite redirect loop. Note that certificate
renewals may fail while proxied; switching back to DNS only fixes that.

Check with `dig +short examigaband.com` (should list the four `185.199.x.153`
addresses while grey-clouded).

### API at api.examigaband.com (Cloudflare Tunnel → Pi)

A Cloudflare Tunnel exposes the Pi without opening ports on the home router or
needing a static IP:

```sh
# on the Pi
cloudflared tunnel login
cloudflared tunnel create examiga
cloudflared tunnel route dns examiga api.examigaband.com   # creates the CNAME
```

`~/.cloudflared/config.yml`:

```yaml
tunnel: examiga
credentials-file: /home/pi/.cloudflared/<tunnel-id>.json
ingress:
  - hostname: api.examigaband.com
    service: http://localhost:80   # nginx, see below
  - service: http_status:404
```

Then `sudo cloudflared service install` to run it under systemd. The API already
enables CORS (`flask-cors`), so the Pages frontend can call it cross-origin.

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
        # Real client IP for the shoutout rate limit (app.py uses ProxyFix).
        proxy_set_header X-Forwarded-For $remote_addr;
    }

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

Drop that (adjusted) into `nginx/conf.d/examiga.conf` when it's time to wire this up.

Behind the Cloudflare Tunnel, add `api.examigaband.com` to `server_name`, and take
the client IP from Cloudflare's header instead: nginx's `$remote_addr` is then
always cloudflared (`127.0.0.1`), so every visitor would share one rate-limit
bucket. Only do this when nginx is reachable solely via the tunnel, since the
header is client-controlled otherwise:

```nginx
        proxy_set_header X-Forwarded-For $http_cf_connecting_ip;
```
