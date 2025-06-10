from django.urls import path
from BlogApi import views
from BlogApi.views import PostPageView

app_name = 'BlogApi'

urlpatterns = [
    path('post/<str:slug>', view=views.PostViews.as_view(), name='post'),
    path('count_pages/<int:post_per_page>', view=views.PostPagesCount.as_view(), name='post_page_count'),
    path('post-page/<int:page_number>', view=PostPageView.as_view(), name='post-page'),
]