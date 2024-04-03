from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.user.models import User
from tests import constants


class TestPostListCreateAPIView:
    def setup_method(self):
        self.client = APIClient()

        user = User.objects.first()
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    def assert_status_code(self, response, expected_status):
        assert response.status_code == expected_status

    def test_create_post(self):
        author_id = User.objects.last().id
        post_data = {"content": constants.POST_EXAMPLE, "author": author_id}
        response = self.client.post(
            reverse("post-list-create"), post_data, format="json"
        )
        self.assert_status_code(response, status.HTTP_201_CREATED)

    def test_create_post_failed_by_author(self):
        author_id = User.objects.last().id + 1
        post_data = {"content": constants.POST_EXAMPLE, "author": author_id}
        response = self.client.post(
            reverse("post-list-create"), post_data, format="json"
        )
        self.assert_status_code(response, status.HTTP_400_BAD_REQUEST)

    def test_create_post_invalid_data(self):
        post_data = {"author": 3}
        response = self.client.post(
            reverse("post-list-create"), post_data, format="json"
        )
        self.assert_status_code(response, status.HTTP_400_BAD_REQUEST)
