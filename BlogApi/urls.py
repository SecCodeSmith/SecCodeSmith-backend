from django.urls import path
from BlogApi.views import *


app_name = 'BlogApi'

urlpatterns = [
    path('post/<str:slug>', view=PostViewsEndpoint.as_view(), name='post'),
    path('related_post/<str:slug>', view=RelatedPostsViewsEndpoint.as_view(), name='related_post'),
    path('count_pages/<int:post_per_page>', view=PostPagesCountEndpoint.as_view(), name='post_page_count'),
    path('post-page/<int:page_number>', view=PostPageViewEndpoint.as_view(), name='post-page'),
    path('tags/', view=TagListsEndpoint.as_view(), name='blog-tags'),
    path('cats/', view=BlogCategoriesEndpoint.as_view(), name='blog-categories'),
]