from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.post.models import Post
from apps.user.models import User


class TestPostDetailAPIView:
    def setup_method(self):
        self.client = APIClient()

        user = User.objects.first()
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    def assert_status_code(self, response, expected_status):
        assert response.status_code == expected_status

    def test_retrieve_single_post(self):
        post = Post.objects.last()
        response = self.client.get(reverse("post-detail", args=[post.id]))
        self.assert_status_code(response, status.HTTP_200_OK)
