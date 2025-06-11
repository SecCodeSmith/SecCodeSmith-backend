from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

import BlogApi
from SecCodeSmithBackend import settings
from api.views import *

urlpatterns = ([
    path('admin/', admin.site.urls),
    path("api/", include("api.urls")),
    path("blog-api/", include("BlogApi.urls")),
    path("img/", include("Images.urls")),
    path("project-api/", include("ProjectApi.urls")),
]
               + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
