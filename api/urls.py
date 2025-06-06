from django.urls import path
from api import views

urlpatterns = [
   path('csrf', views.CSRFTokenView.as_view(), name='csrf'),
    path('skills-cards', views.SkillCards.as_view(), name='skills-cards'),
    path('about/<str:lang>/', views.AboutPage.as_view(), name='about'),
]