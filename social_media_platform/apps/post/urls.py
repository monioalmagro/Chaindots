from django.urls import path

from apps.post.views import CommentListAPIView, PostDetailAPIView, PostListCreateAPIView

urlpatterns = [
    path("api/posts/", PostListCreateAPIView.as_view(), name="post-list-create"),
    path("api/posts/<int:id>/", PostDetailAPIView.as_view(), name="post-detail"),
    path(
        "api/posts/<int:id>/comments/",
        CommentListAPIView.as_view(),
        name="comments-list",
    ),
]
