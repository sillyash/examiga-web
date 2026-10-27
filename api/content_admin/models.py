from django.db import models


class TourDate(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    city = models.CharField(max_length=120)
    venue = models.CharField(max_length=160)
    address = models.CharField(max_length=200, null=True, blank=True)
    ticket_url = models.CharField(max_length=300, null=True, blank=True)
    info_url = models.CharField(max_length=300, null=True, blank=True)
    is_sold_out = models.BooleanField(default=False)
    notes = models.CharField(max_length=300, null=True, blank=True)

    class Meta:
        managed = False
        db_table = "tour_dates"
        ordering = ("date", "id")
        verbose_name = "tour date"
        verbose_name_plural = "tour dates"

    def __str__(self):
        return f"{self.date} - {self.city}, {self.venue}"


class Shoutout(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80)
    message = models.TextField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "shoutouts"
        ordering = ("-created_at", "-id")

    def __str__(self):
        return f"{self.name}: {self.message[:60]}"
