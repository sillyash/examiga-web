from datetime import date, datetime, time
import os

from app import create_app
from db import db
from models import Shoutout, TourDate

# Optional starter data for a fresh development database. Existing tour dates are
# updated by matching date, city, and venue; rows omitted from this list are kept.
TOUR_DATES = [
    dict(
        date=date(2026, 10, 9),
        time=time(20, 0),
        city="Paris",
        venue="La Pointe Lafayette",
        address="230 Rue La Fayette, Paris, FR 75010",
        ticket_url=None,
        info_url=None,
        is_sold_out=False,
        notes="w/ Pericolo !!",
    ),
    dict(
        date=date(2026, 10, 10),
        time=None,
        city="Paris",
        venue="La Maz",
        address="9 rue Turbigo 75001 Paris",
        ticket_url=None,
        info_url="https://www.instagram.com/p/Dd6kf-0RCPq/",
        is_sold_out=False,
        notes="Co-plateau ! Interested ? Reach contact@examigaband.com",
    ),
    dict(
        date=date(2026, 9, 8),
        time=time(19, 30),
        city="Palaiseau",
        venue="Télécom Paris",
        address="19 Place Marguerite Perey, 91120 Palaiseau",
        ticket_url=None,
        info_url=None,
        is_sold_out=False,
        notes="Téléfest :3",
    ),
]

# Demo shoutouts for a fresh dev DB. Real ones come in through the public
# POST /api/shoutouts endpoint, so this only fills the table when it's empty.
SHOUTOUTS = [
    dict(
        name="AlexCharp",
        message="Venez à Evry!!! On a besoin de emo ici aussi...",
        created_at=datetime(2026, 9, 5, 9, 12),
    ),
]


def seed():
    if os.environ.get("EXAMIGA_DB_PATH") and os.environ.get("ALLOW_CONFIGURED_DB_SEED") != "true":
        raise SystemExit(
            "Refusing to seed a configured database. Set ALLOW_CONFIGURED_DB_SEED=true "
            "to explicitly allow updates to EXAMIGA_DB_PATH."
        )

    app = create_app()
    with app.app_context():
        for tour_date in TOUR_DATES:
            existing = TourDate.query.filter_by(
                date=tour_date["date"],
                city=tour_date["city"],
                venue=tour_date["venue"],
            ).first()
            if existing is None:
                db.session.add(TourDate(**tour_date))
            else:
                for field, value in tour_date.items():
                    setattr(existing, field, value)

        if Shoutout.query.count() == 0:
            db.session.bulk_insert_mappings(Shoutout, SHOUTOUTS)

        db.session.commit()
        print(f"Updated or added {len(TOUR_DATES)} starter tour dates.")


if __name__ == "__main__":
    seed()
