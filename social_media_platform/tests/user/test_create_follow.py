from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.user.models import User


class TestUserCreateFollowAPIView:
    def setup_method(self):
        self.client = APIClient()

        user = User.objects.first()
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    def assert_status_code(self, response, expected_status):
        assert response.status_code == expected_status

    def test_create_follow_success(self):
        user_1 = User.objects.first()
        user_2 = User.objects.last()

        user_2.unfollow(user_1)

        response = self.client.post(
            reverse(
                "create-follow",
                kwargs={"follower_id": user_2.id, "followee_id": user_1.id},
            ),
            data={},
            format="json",
        )
        self.assert_status_code(response, status.HTTP_200_OK)
        assert "You are now following this user" in response.data["message"]

        assert user_1.is_followed_by(user_2)

    def test_create_follow_fail_self_follow(self):

        user = User.objects.last()

        response = self.client.post(
            reverse(
                "create-follow", kwargs={"follower_id": user.id, "followee_id": user.id}
            ),
            data={},
            format="json",
        )

        self.assert_status_code(response, status.HTTP_400_BAD_REQUEST)
        assert "Cannot follow yourself" in response.data["error"]

    def test_create_follow_fail_already_following(self):

        follower = User.objects.last()
        followee = User.objects.first()

        follower.following.add(followee)

        response = self.client.post(
            reverse(
                "create-follow",
                kwargs={"follower_id": follower.id, "followee_id": followee.id},
            ),
            data={},
            format="json",
        )

        self.assert_status_code(response, status.HTTP_400_BAD_REQUEST)
        assert "Already following this user" in response.data["error"]
