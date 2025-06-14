from django.urls import path
from api import views

urlpatterns = [
   path('csrf', views.CSRFTokenView.as_view(), name='csrf'),
    path('skills-cards', views.SkillCards.as_view(), name='skills-cards'),
    path('about/<str:lang>/', views.AboutPage.as_view(), name='about'),
    path('about/', views.AboutPage.as_view(), name='about_default'),
    path('footer-links', views.SocialLinksFooter.as_view(), name='social-links-footer'),
    path('contact/<str:lang_arg>', views.ContactPage.as_view(), name='contact'),
    path('contact/', views.ContactPage.as_view(), name='contact_default'),
]