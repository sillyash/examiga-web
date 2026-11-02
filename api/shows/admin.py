from django.contrib import admin

from .models import Shoutout, TourDate


@admin.register(TourDate)
class TourDateAdmin(admin.ModelAdmin):
    list_display = ["date", "time", "city", "venue", "is_sold_out"]


@admin.register(Shoutout)
class ShoutoutAdmin(admin.ModelAdmin):
    list_display = ["name", "message", "created_at"]
    search_fields = ["name", "message"]
