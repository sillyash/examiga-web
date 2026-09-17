from datetime import datetime

from db import db


class TourDate(db.Model):
    __tablename__ = "tour_dates"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    venue = db.Column(db.String(160), nullable=False)
    ticket_url = db.Column(db.String(300))
    is_sold_out = db.Column(db.Boolean, nullable=False, default=False)
    notes = db.Column(db.String(300))


class Shoutout(db.Model):
    __tablename__ = "shoutouts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
