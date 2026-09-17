from pathlib import Path

from apiflask import APIFlask
from flask_cors import CORS

from db import db
from models import Shoutout, TourDate
from schemas import ShoutoutIn, ShoutoutOut, TourDateOut

BASE_DIR = Path(__file__).resolve().parent


def create_app():
    app = APIFlask(__name__, title="EX-AMIGA API", version="1.0.0")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{BASE_DIR / 'examiga.db'}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    CORS(app)

    with app.app_context():
        db.create_all()

    @app.get("/api/tour-dates")
    @app.output(TourDateOut(many=True))
    @app.doc(tags=["Tour dates"])
    def list_tour_dates():
        """List all tour dates, soonest first."""
        return TourDate.query.order_by(TourDate.date.asc()).all()

    @app.get("/api/shoutouts")
    @app.output(ShoutoutOut(many=True))
    @app.doc(tags=["Shoutouts"])
    def list_shoutouts():
        """List all fan shoutouts, newest first."""
        return Shoutout.query.order_by(Shoutout.created_at.desc()).all()

    @app.post("/api/shoutouts")
    @app.input(ShoutoutIn)
    @app.output(ShoutoutOut, status_code=201)
    @app.doc(tags=["Shoutouts"])
    def create_shoutout(json_data):
        """Leave a shoutout for the band."""
        shoutout = Shoutout(name=json_data["name"], message=json_data["message"])
        db.session.add(shoutout)
        db.session.commit()
        return shoutout

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
