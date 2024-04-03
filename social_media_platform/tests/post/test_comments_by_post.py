import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.comment.models import Comment
from apps.post.models import Post
from apps.user.models import User


@pytest.mark.django_db
class TestCommentListAPIView:
    def setup_method(self):
        self.client = APIClient()

        user = User.objects.first()
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    def assert_status_code(self, response, expected_status):
        assert response.status_code == expected_status

    def test_get_comments_for_post(self):

        comment = Comment.objects.last()
        post = comment.post_id

        response = self.client.get(reverse("comments-list", kwargs={"id": post}))
        self.assert_status_code(response, status.HTTP_200_OK)

        assert response.data["comments"][0]["content"] == comment.content

    def test_get_comments_for_nonexistent_post(self):
        response = self.client.get(reverse("comments-list", kwargs={"id": 999}))
        self.assert_status_code(response, status.HTTP_404_NOT_FOUND)

    def test_create_comment(self):
        post = Post.objects.last()
        user = post.author_id

        comment_data = {"author_id": user, "comment": "Test comment"}
        response = self.client.post(
            reverse("comments-list", kwargs={"id": post.id}),
            comment_data,
            format="json",
        )
        self.assert_status_code(response, status.HTTP_201_CREATED)
        assert Comment.objects.filter(post=post, content="Test comment").exists()

    def test_create_comment_with_invalid_data(self):
        post = Post.objects.last()
        user = post.author_id

        comment_data = {"author_id": user}
        response = self.client.post(
            reverse("comments-list", kwargs={"id": post.id}),
            comment_data,
            format="json",
        )
        self.assert_status_code(response, status.HTTP_400_BAD_REQUEST)
