from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("home.urls")),
    path('login/', include("home.urls")),
    path('boost/', include("boost.urls")),
    path('expenses/', include("boost.urls")),
    path('register/', include("home.urls")),
    path("admin/", admin.site.urls),
]