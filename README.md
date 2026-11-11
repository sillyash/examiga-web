# EX-AMIGA

Website for EX-AMIGA, a midwest emo band: tour dates and a fan shoutouts/guestbook.

Live version: https://examigaband.com

## Getting started (development)

### Prerequisites

- [Node.js](https://nodejs.org/) 22.18+ or 24.12+
- [uv](https://docs.astral.sh/uv/getting-started/installation/), Python package manager.
- [just](https://just.systems/man/en/packages.html), CLI tool for easy commands

### Steps

1. Clone the repository

```bash
git clone https://github.com/sillyash/examiga-web.git
cd examiga-web
```

2. Install dependencies

```bash
just install
```

3. Create the database (migrations load `api/backup/*.json`)

```bash
just migrate
```

4. Start development servers (API + frontend)

```bash
just dev
```

5. Open http://localhost:5173 in your browser. The admin is at http://localhost:5000/admin/
   (create a login with `just superuser`).

The graded school submission (Flask API, see `docs/rapport.pdf`) is tagged `rapport`.

## More

List commands:

```bash
just
```

- [web/README.md](web/README.md) - frontend (Vue 3 + TypeScript)
- [api/README.md](api/README.md) - backend (Django API + admin)
- [DEPLOYMENT.md](DEPLOYMENT.md) - hosting on GitHub Pages / a Raspberry Pi

## License

MIT, see [LICENSE](LICENSE).
