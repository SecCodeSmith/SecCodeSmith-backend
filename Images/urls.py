from django.urls import path
from .views import *

app_name = "core"

urlpatterns = [
    path("Image/", ImageProps.as_view(), name="image_list"),
]
