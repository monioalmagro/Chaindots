from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.user.models import User


class TestCreateUser:
    def setup_method(self):
        self.client = APIClient()

        user = User.objects.first()
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    def assert_status_code(self, response, expected_status):
        assert response.status_code == expected_status

    def test_retrieve_all_users(self):
        user = User.objects.last()
        user_data = {
            "username": user.username,
            "email": user.email,
            "password": user.password,
        }
        user.delete()
        response = self.client.post(reverse("users-list"), user_data, format="json")
        self.assert_status_code(response, status.HTTP_201_CREATED)
