from datetime import date, datetime

from app import create_app
from db import db
from models import Shoutout, TourDate

# Source of truth for tour dates: edit this list and rerun `uv run python seed.py`
# to update the site. Every run replaces the whole tour_dates table with this list.
TOUR_DATES = [
    dict(
        date=date(2026, 10, 3),
        city="Chicago, IL",
        venue="The Rathskeller",
        ticket_url="https://example.com/tickets/chicago",
        is_sold_out=False,
        notes="w/ Static Orchard, Fencewalker",
    ),
    dict(
        date=date(2026, 10, 14),
        city="Columbus, OH",
        venue="Cafe Mustache",
        ticket_url="https://example.com/tickets/columbus",
        is_sold_out=True,
        notes=None,
    ),
    dict(
        date=date(2026, 11, 8),
        city="St. Louis, MO",
        venue="Foam House",
        ticket_url=None,
        is_sold_out=False,
        notes="DIY all-ages show",
    ),
    dict(
        date=date(2026, 12, 10),
        city="Kansas City, MO",
        venue="The Tin Ceiling",
        ticket_url="https://example.com/tickets/kc",
        is_sold_out=False,
        notes="w/ Static Orchard",
    ),
]

# Demo shoutouts for a fresh dev DB. Real ones come in through the public
# POST /api/shoutouts endpoint, so this only fills the table when it's empty.
SHOUTOUTS = [
    dict(
        name="Casey54",
        message="Saw you guys in a basement in 2019, still think about that set weekly.",
        created_at=datetime(2026, 9, 1, 14, 32),
    ),
    dict(
        name="Jordan",
        message="Please come to Cleveland!!! we need midwest emo out here too",
        created_at=datetime(2026, 9, 5, 9, 12),
    ),
    dict(
        name="Rileyyy",
        message="the new EP has been on repeat since it dropped, twinkly riffs go crazy",
        created_at=datetime(2026, 9, 10, 20, 45),
    ),
    dict(
        name="Sam",
        message="thank you for playing that one song that made me cry in a Guitar Center parking lot",
        created_at=datetime(2026, 9, 14, 23, 58),
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
