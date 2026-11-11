from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from shows.api import router

urlpatterns = [
    path("api/", include(router.urls)),
    path("admin/", admin.site.urls),
    path("openapi.json", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema")),
]
