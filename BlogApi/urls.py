from django.urls import path

from BlogApi.views import *

app_name = "BlogApi"

urlpatterns = [
    path("post/<str:slug>", view=PostViewsEndpoint.as_view(), name="post"),
    path("post/", view=PostViewsEndpoint.as_view(), name="post_without_slug"),
    path(
        "related-posts/<str:category_slug>",
        view=RelatedPostsViewsEndpoint.as_view(),
        name="related_post",
    ),
    path(
        "related-posts/",
        view=RelatedPostsViewsEndpoint.as_view(),
        name="related-posts_without_slug",
    ),
    path(
        "count_pages/<int:post_per_page>",
        view=PostPagesCountEndpoint.as_view(),
        name="post_page_count",
    ),
    path(
        "post-page/<int:page_number>",
        view=PostPageViewEndpoint.as_view(),
        name="post-page",
    ),
    path("tags/", view=TagListsEndpoint.as_view(), name="blog-tags"),
    path("cats/", view=BlogCategoriesEndpoint.as_view(), name="blog-categories"),
]
