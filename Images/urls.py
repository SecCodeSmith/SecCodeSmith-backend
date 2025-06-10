from django.urls import path
from Images.views import *

app_name = "image"

urlpatterns = [
    path("Image/<str:name>/", ImageProps.as_view(), name="image_list"),
]
