# EX-AMIGA API

Flask + SQLAlchemy backend (tour dates + shoutouts), managed with
[uv](https://docs.astral.sh/uv/).

## Install

```sh
uv sync
```

## Run (dev)

```sh
uv run python seed.py   # (re)populate tour dates from seed.py; first run also seeds demo shoutouts
uv run python app.py    # http://localhost:5000
```

## Run (prod)

```sh
uv run gunicorn --bind 0.0.0.0:5000 app:app
```
