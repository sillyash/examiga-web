from pathlib import Path

from apiflask import APIFlask
from flask_cors import CORS
from flask import redirect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from sqlalchemy import tuple_
from werkzeug.middleware.proxy_fix import ProxyFix

from db import db
from models import Shoutout, TourDate
from schemas import ShoutoutIn, ShoutoutOut, ShoutoutPage, ShoutoutQuery, TourDateOut

BASE_DIR = Path(__file__).resolve().parent

# Per-IP rate limits. In-memory storage is fine: deployment runs a single gunicorn
# worker (see DEPLOYMENT.md); counters reset on restart.
limiter = Limiter(get_remote_address, storage_uri="memory://")


def create_app():
    app = APIFlask(__name__, title="EX-AMIGA API", version="1.0.0")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{BASE_DIR / 'examiga.db'}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Behind nginx every request comes from 127.0.0.1; trust its X-Forwarded-For so
    # rate limiting sees the real client IP. Gunicorn only listens on localhost, so
    # the header can't be spoofed from outside.
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)

    db.init_app(app)
    limiter.init_app(app)
    CORS(app)

    with app.app_context():
        db.create_all()

    @app.get("/")
    @app.doc(hide=True)
    def index():
        return redirect("/docs")

    @app.get("/api/tour-dates")
    @app.output(TourDateOut(many=True))
    @app.doc(tags=["Tour dates"])
    def list_tour_dates():
        """List all tour dates, soonest first."""
        return TourDate.query.order_by(TourDate.date.asc()).all()

    @app.get("/api/shoutouts")
    @app.input(ShoutoutQuery, location="query")
    @app.output(ShoutoutPage)
    @app.doc(tags=["Shoutouts"])
    def list_shoutouts(query_data):
        """List fan shoutouts, newest first, `limit` at a time.

        Pass the id of the last shoutout you got as `before` to load the next page.
        """
        query = Shoutout.query.order_by(Shoutout.created_at.desc(), Shoutout.id.desc())

        if query_data["before"] is not None:
            cursor = db.get_or_404(Shoutout, query_data["before"])
            # Strictly older than the cursor; id breaks ties on equal timestamps.
            query = query.filter(
                tuple_(Shoutout.created_at, Shoutout.id) < (cursor.created_at, cursor.id)
            )

        # Fetch one extra row to know whether there's another page after this one.
        rows = query.limit(query_data["limit"] + 1).all()
        return {
            "shoutouts": rows[: query_data["limit"]],
            "has_more": len(rows) > query_data["limit"],
        }

    @app.post("/api/shoutouts")
    @limiter.limit("3 per minute; 20 per day")
    @app.input(ShoutoutIn)
    @app.output(ShoutoutOut, status_code=201)
    @app.doc(tags=["Shoutouts"])
    def create_shoutout(json_data):
        """Leave a shoutout for the band.

        Limited to 3 per minute and 20 per day per IP (429 past that).
        """
        shoutout = Shoutout(name=json_data["name"], message=json_data["message"])
        db.session.add(shoutout)
        db.session.commit()
        return shoutout

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
