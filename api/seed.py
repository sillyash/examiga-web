from datetime import date, datetime, time

from app import create_app
from db import db
from models import Shoutout, TourDate

# Source of truth for tour dates: edit this list and rerun `uv run python seed.py`
# to update the site. Every run replaces the whole tour_dates table with this list.
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
        info_url=None,
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
    app = create_app()
    with app.app_context():
        TourDate.query.delete()
        db.session.bulk_insert_mappings(TourDate, TOUR_DATES)

        if Shoutout.query.count() == 0:
            db.session.bulk_insert_mappings(Shoutout, SHOUTOUTS)

        db.session.commit()
        print(f"Seeded {len(TOUR_DATES)} tour dates.")


if __name__ == "__main__":
    seed()
