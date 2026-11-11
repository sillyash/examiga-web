# EX-AMIGA

Website for EX-AMIGA, a midwest emo band: tour dates and a fan shoutouts/guestbook.

Live version: https://examigaband.com

## Getting started (development)

### Prerequisites

- [Node.js](https://nodejs.org/) 22.18+ or 24.12+
- [uv](https://docs.astral.sh/uv/getting-started/installation/), Python package manager.
- [just](https://just.systems/man/en/packages.html), CLI tool for easy commands

### Steps

1. Extract the archive and go into the project folder

```bash
tar -xzf merienne_ashley_vuejs.tar.gz
cd merienne_ashley_vuejs
```

2. Install dependencies

```bash
just install
```

3. Seed database

```bash
just seed
```

4. Start development servers (API + frontend)

```bash
just dev
```

5. Open http://localhost:5173 in your browser.

## More

List commands:

```bash
just
```

- [web/README.md](web/README.md) - frontend (Vue 3 + TypeScript)
- [api/README.md](api/README.md) - backend (Flask + SQLAlchemy)
- [DEPLOYMENT.md](DEPLOYMENT.md) - hosting on GitHub Pages / a Raspberry Pi

## License

MIT, see [LICENSE](LICENSE).
