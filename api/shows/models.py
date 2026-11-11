from django.db import models
from django.utils import timezone


class TourDate(models.Model):
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    city = models.CharField(max_length=120)
    venue = models.CharField(max_length=160)
    address = models.CharField(max_length=200, null=True, blank=True)
    ticket_url = models.URLField(max_length=300, null=True, blank=True)
    info_url = models.URLField(max_length=300, null=True, blank=True)
    is_sold_out = models.BooleanField(default=False)
    notes = models.CharField(max_length=300, null=True, blank=True)

    class Meta:
        ordering = ["date", "id"]

    def __str__(self):
        return f"{self.date} {self.city}, {self.venue}"


class Shoutout(models.Model):
    name = models.CharField(max_length=80)
    message = models.TextField(max_length=500)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        ordering = ["-created_at", "-id"]

    def __str__(self):
        return f"{self.name}: {self.message[:60]}"
