from rest_framework import mixins, serializers, viewsets
from rest_framework.pagination import CursorPagination
from rest_framework.routers import SimpleRouter
from rest_framework.throttling import AnonRateThrottle

from .models import Shoutout, TourDate


class TourDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourDate
        fields = "__all__"


class ShoutoutSerializer(serializers.ModelSerializer):
    # Honeypot: hidden in the form, so only bots fill it in.
    website = serializers.CharField(write_only=True, required=False, allow_blank=True, max_length=0)

    class Meta:
        model = Shoutout
        fields = ["id", "name", "message", "created_at", "website"]

    def create(self, validated_data):
        validated_data.pop("website", None)
        return super().create(validated_data)


class ShoutoutMinuteThrottle(AnonRateThrottle):
    scope = "shoutout_minute"


class ShoutoutDayThrottle(AnonRateThrottle):
    scope = "shoutout_day"


class ShoutoutPagination(CursorPagination):
    page_size = 10
    ordering = ["-created_at", "-id"]


class TourDateViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = TourDate.objects.all()
    serializer_class = TourDateSerializer


class ShoutoutViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Shoutout.objects.all()
    serializer_class = ShoutoutSerializer
    pagination_class = ShoutoutPagination

    def get_throttles(self):
        if self.action == "create":
            return [ShoutoutMinuteThrottle(), ShoutoutDayThrottle()]
        return []


router = SimpleRouter(trailing_slash=False)
router.register("tour-dates", TourDateViewSet)
router.register("shoutouts", ShoutoutViewSet)
