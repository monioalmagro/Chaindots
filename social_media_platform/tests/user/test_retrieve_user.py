from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.comment.models import Comment
from apps.post.models import Post
from apps.user.models import User


class TestRetieveUserAPIView:
    def setup_method(self):
        self.client = APIClient()

        user = User.objects.first()
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    def assert_status_code(self, response, expected_status):
        assert response.status_code == expected_status

    def test_retrieve_all_users(self):
        response = self.client.get(reverse("users-list"))
        self.assert_status_code(response, status.HTTP_200_OK)

    def test_retrieve_existing_user(self):
        user = User.objects.last()

        response = self.client.get(reverse("user-detail", kwargs={"user_id": user.id}))

        self.assert_status_code(response, status.HTTP_200_OK)
        assert response.data["username"] == user.username
        assert response.data["email"] == user.email

    def test_retrieve_non_existent_user(self):
        response = self.client.get(reverse("user-detail", kwargs={"user_id": 999}))

        self.assert_status_code(response, status.HTTP_404_NOT_FOUND)

    def test_post_comment_counts(self):
        user = User.objects.last()

        posts = Post.objects.filter(author_id=user.id)
        posts_ids = posts.values_list("id", flat=True)

        comments = Comment.objects.filter(post_id__in=posts_ids)

        response = self.client.get(reverse("user-detail", kwargs={"user_id": user.id}))

        self.assert_status_code(response, status.HTTP_200_OK)
        assert response.data["total_posts"] == posts.count()
        assert response.data["total_comments"] == comments.count()
