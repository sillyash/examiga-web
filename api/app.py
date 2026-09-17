from pathlib import Path

from flask import Flask, jsonify, request
from flask_cors import CORS

from db import db
from models import Shoutout, TourDate

BASE_DIR = Path(__file__).resolve().parent


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{BASE_DIR / 'examiga.db'}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    CORS(app)

    with app.app_context():
        db.create_all()

    @app.get("/api/tour-dates")
    def list_tour_dates():
        tour_dates = TourDate.query.order_by(TourDate.date.asc()).all()
        return jsonify([t.to_dict() for t in tour_dates])

    @app.get("/api/shoutouts")
    def list_shoutouts():
        shoutouts = Shoutout.query.order_by(Shoutout.created_at.desc()).all()
        return jsonify([s.to_dict() for s in shoutouts])

    @app.post("/api/shoutouts")
    def create_shoutout():
        payload = request.get_json(silent=True) or {}
        name = (payload.get("name") or "").strip()
        message = (payload.get("message") or "").strip()
        if not name or not message:
            return jsonify({"error": "name and message are required"}), 400

        shoutout = Shoutout(name=name[:80], message=message)
        db.session.add(shoutout)
        db.session.commit()
        return jsonify(shoutout.to_dict()), 201

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
