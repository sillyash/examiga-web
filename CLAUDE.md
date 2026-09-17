# examiga-web

EX-AMIGA is the website for a midwest emo band: tour dates and a fan
shoutouts/guestbook. MIT licensed.

**This is graded ENSIIE coursework** ("Bases du Web"), not just a hobby project — see
the school-project-constraints memory for the full spec (file/table/page/size limits,
required buttons, grading rubric). Final submission archive:
`merienne_ashley_vuejs.tar.gz`, built by `scripts/package.sh`.

## Repo layout

- `web/` — Vue 3 + TypeScript frontend (see below).
- `api/` — Flask + SQLAlchemy backend (see below), managed with **uv**.
- `scripts/` — `md_to_pdf.sh` (renders `docs/RAPPORT.md` → `docs/rapport.pdf` via
  pandoc + pdflatex) and `package.sh` (builds the frontend as a smoke test, then stages
  and tars/gzips the whole repo into `merienne_ashley_vuejs.tar.gz`, excluding
  `node_modules`, `.venv`, `__pycache__`, `*.db`, `.git`, `CLAUDE.md`).
- `docs/RAPPORT.md` — empty. Given the default `fr` locale in the frontend and the
  "RAPPORT" naming, this is the French-language project report source, rendered to PDF
  by `scripts/md_to_pdf.sh`.
- `README.md` (root) — links out to `web/README.md`, `api/README.md`, `DEPLOYMENT.md`.
- `DEPLOYMENT.md` — real-world hosting (GitHub Pages / Raspberry Pi).

## Frontend stack (`web/`)

Default `create-vue` scaffold, essentially untouched from the generator:

- **Vue 3.5** + **TypeScript ~6.0** (type-checked via `vue-tsc`, since `tsc` can't
  handle `.vue` imports directly)
- **Vite 8.2** as the build tool/dev server, with `@` aliased to `web/src/`
- **Pinia 4** for state (only store so far is the generator's demo `stores/counter.ts`)
- **Vue Router 5** (`src/router/index.ts`) — routes array is currently empty
- **vue-i18n** (locale `fr`, fallback `en`), wired up in `main.ts` — not yet used for
  the assignment's required language-toggle button
- Linting/formatting: **oxlint** + **eslint** (`eslint-plugin-vue`, `eslint-plugin-oxlint`)
  + **Prettier**
- Day/night theming: `src/composables/useTheme.ts` (module-scoped `ref`, persisted to
  `localStorage`, falls back to `prefers-color-scheme`) sets `data-theme` on
  `<html>`; `src/assets/main.css` defines the light/dark CSS custom properties;
  `src/components/ThemeToggle.vue` is the toggle button, mounted in `App.vue`'s
  header so it's present on every page. Chose a composable over a Pinia store since
  it's a single global flag — simpler, and reactivity works fine at module scope.

Commands (run from `web/`):
```
npm run dev           # vite dev server
npm run build         # type-check + vite build
npm run preview       # preview production build
npm run type-check    # vue-tsc --build
npm run lint          # oxlint --fix && eslint --fix
npm run format        # prettier --write src/
```

## Backend stack (`api/`)

**APIFlask** (Flask + Flask-SQLAlchemy + marshmallow) on SQLite, dependency-managed
with **uv** (`pyproject.toml` + `uv.lock`, not pip/requirements.txt). No Dockerfile —
deployment runs `uv run gunicorn` directly, see `DEPLOYMENT.md`.

- `models.py` — `TourDate`, `Shoutout` (plain SQLAlchemy models, no `to_dict()` —
  serialization lives in `schemas.py` now).
- `schemas.py` — marshmallow schemas (`TourDateOut`, `ShoutoutIn`, `ShoutoutOut`) used
  by `app.py`'s `@app.input`/`@app.output` decorators for validation + serialization.
- `app.py` — routes tagged/documented for APIFlask's auto-generated OpenAPI spec:
  Swagger UI at `/docs`, raw spec at `/openapi.json`. Invalid POST bodies get a 422
  with field-level errors for free (via marshmallow), not the old manual 400 checks.

> [!NOTE]
> `POST /api/shoutouts` has no auth — it's a public guestbook, that's the point.

