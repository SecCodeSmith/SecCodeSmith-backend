from django.contrib import admin
from django.urls import path
from SecCodeSmithBackend.views import CSRFTokenView, GetSkillListsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/csrf-token/', CSRFTokenView.as_view(), name='csrf_token'),
    path('api/skill-lists/', GetSkillListsView.as_view(), name='get_skill_lists'),
]
