import json
from datetime import UTC
from pathlib import Path

from django.db import migrations
from django.utils.dateparse import parse_datetime

BACKUP_DIR = Path(__file__).resolve().parents[2] / "backup"


def load(apps, schema_editor):
    TourDate = apps.get_model("shows", "TourDate")
    Shoutout = apps.get_model("shows", "Shoutout")
    tour_dates = json.loads((BACKUP_DIR / "tour-dates.json").read_text())
    shoutouts = json.loads((BACKUP_DIR / "shoutouts.json").read_text())["shoutouts"]
    TourDate.objects.bulk_create(TourDate(**row) for row in tour_dates)
    Shoutout.objects.bulk_create(
        Shoutout(**{**row, "created_at": aware(row["created_at"])}) for row in shoutouts
    )


def aware(value):
    # The old API stored naive UTC timestamps.
    dt = parse_datetime(value)
    return dt if dt.tzinfo else dt.replace(tzinfo=UTC)


def unload(apps, schema_editor):
    apps.get_model("shows", "TourDate").objects.all().delete()
    apps.get_model("shows", "Shoutout").objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [("shows", "0001_initial")]
    operations = [migrations.RunPython(load, unload)]
