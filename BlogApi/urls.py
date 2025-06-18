from django.urls import path
from BlogApi.views import *


app_name = 'BlogApi'

urlpatterns = [
    path('post/<str:slug>', view=PostViews.as_view(), name='post'),
    path('count_pages/<int:post_per_page>', view=PostPagesCount.as_view(), name='post_page_count'),
    path('post-page/<int:page_number>', view=PostPageView.as_view(), name='post-page'),
    path('tags/', view=TagLists.as_view(), name='blog-tags'),
]