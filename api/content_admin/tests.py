from datetime import date, datetime

from django.contrib.auth import get_user_model
from django.db import connection
from django.test import TransactionTestCase
from django.urls import reverse

from content_admin.models import Shoutout, TourDate


class ContentAdminTests(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with connection.schema_editor() as editor:
            editor.create_model(TourDate)
            editor.create_model(Shoutout)

    @classmethod
    def tearDownClass(cls):
        with connection.schema_editor() as editor:
            editor.delete_model(Shoutout)
            editor.delete_model(TourDate)
        super().tearDownClass()

    def setUp(self):
        TourDate.objects.all().delete()
        Shoutout.objects.all().delete()
        self.admin = get_user_model().objects.create_superuser(
            username="admin", email="admin@example.test", password="test-password"
        )

    def test_admin_requires_authentication(self):
        response = self.client.get(reverse("admin:index"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("admin:login"), response["Location"])

    def test_admin_can_create_tour_date(self):
        self.client.force_login(self.admin)

        response = self.client.post(
            reverse("admin:content_admin_tourdate_add"),
            {
                "date": "2027-05-01",
                "time": "",
                "city": "Chicago",
                "venue": "Metro",
                "address": "3730 N Clark St",
                "ticket_url": "",
                "info_url": "",
                "is_sold_out": "",
                "notes": "",
                "_save": "Save",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            TourDate.objects.filter(date=date(2027, 5, 1), city="Chicago", venue="Metro").exists()
        )

    def test_admin_can_edit_tour_date(self):
        tour_date = TourDate.objects.create(
            date=date(2027, 5, 1), city="Chicago", venue="Metro", is_sold_out=False
        )
        self.client.force_login(self.admin)

        response = self.client.post(
            reverse("admin:content_admin_tourdate_change", args=(tour_date.pk,)),
            {
                "date": "2027-05-01",
                "time": "",
                "city": "Milwaukee",
                "venue": "Cactus Club",
                "address": "2496 S Wentworth Ave",
                "ticket_url": "",
                "info_url": "",
                "is_sold_out": "on",
                "notes": "Updated show",
                "_save": "Save",
            },
        )

        self.assertEqual(response.status_code, 302)
        tour_date.refresh_from_db()
        self.assertEqual(tour_date.city, "Milwaukee")
        self.assertTrue(tour_date.is_sold_out)

    def test_admin_can_delete_shoutout(self):
        shoutout = Shoutout.objects.create(
            name="Listener",
            message="Great show",
            created_at=datetime(2026, 10, 1, 12, 0),
        )
        self.client.force_login(self.admin)

        response = self.client.post(
            reverse("admin:content_admin_shoutout_delete", args=(shoutout.pk,)),
            {"post": "yes"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Shoutout.objects.filter(pk=shoutout.pk).exists())
