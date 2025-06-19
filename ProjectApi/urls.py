from django.urls import path
from .views import *

app_name = "projects"

urlpatterns = [
    path('projects/', view=ProjectsEndpoint.as_view(), name='projects'),
    path('projects/<int:project_id>/', view=ProjectDetailEndpoint.as_view(), name='project-detail'),
    path('cats/', view=ProjectCategoryEndpoint.as_view(), name='project-category'),
]
