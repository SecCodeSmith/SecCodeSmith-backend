from django.contrib import admin
from django.urls import include, path

import BlogApi
from api.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("api.urls")),
    path("blog-api/", include("BlogApi.urls")),
    path("img/", include("Images.urls")),
]
