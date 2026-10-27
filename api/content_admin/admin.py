from django.contrib import admin

from .models import Shoutout, TourDate


@admin.register(TourDate)
class TourDateAdmin(admin.ModelAdmin):
    list_display = ("date", "time", "city", "venue", "is_sold_out")
    list_filter = ("is_sold_out", "date")
    search_fields = ("city", "venue", "address", "notes")
    ordering = ("date", "id")
    date_hierarchy = "date"


@admin.register(Shoutout)
class ShoutoutAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "message_preview")
    list_filter = ("created_at",)
    search_fields = ("name", "message")
    ordering = ("-created_at", "-id")
    date_hierarchy = "created_at"
    readonly_fields = ("created_at",)
    fields = ("name", "message", "created_at")

    @admin.display(description="Message")
    def message_preview(self, shoutout):
        return shoutout.message[:100]
