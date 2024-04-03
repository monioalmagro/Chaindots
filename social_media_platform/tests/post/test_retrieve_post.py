from datetime import datetime, timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.post.models import Post
from apps.user.models import User


class TestRetievePostAPIView:
    def setup_method(self):
        self.client = APIClient()

        user = User.objects.first()
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    def assert_status_code(self, response, expected_status):
        assert response.status_code == expected_status

    def test_retrieve_all_posts(self):
        response = self.client.get(reverse("post-list-create"))
        self.assert_status_code(response, status.HTTP_200_OK)

    def test_retrieve_single_post(self):
        post = Post.objects.first()
        response = self.client.get(reverse("post-detail", args=[post.id]))
        self.assert_status_code(response, status.HTTP_200_OK)

    def test_retrieve_all_posts_ordered(self):
        response = self.client.get(reverse("post-list-create"))
        self.assert_status_code(response, status.HTTP_200_OK)
        posts = response.data
        for i in range(len(posts) - 1):
            assert posts[i]["created_at"] >= posts[i + 1]["created_at"]

    def test_retrieve_all_posts_filtered_by_author_id(self):
        author_id = User.objects.last().id
        response = self.client.get(f"/api/posts/?author_id={author_id}", format="json")
        self.assert_status_code(response, status.HTTP_200_OK)
        posts = response.data
        for post in posts:
            assert post["author"] == author_id

    def test_retrieve_all_posts_filtered_by_date_range(self):
        today = timezone.now().date()
        from_date = today - timedelta(days=7)
        to_date = today
        response = self.client.get(
            f"/api/posts/?from_date={from_date}&to_date={to_date}", format="json"
        )
        self.assert_status_code(response, status.HTTP_200_OK)
        posts = response.data
        for post in posts:
            created_at = datetime.strptime(
                post["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ"
            ).date()
            assert from_date <= created_at <= to_date

    def test_retrieve_all_posts_with_pagination_and_default_parameters(self):
        response = self.client.get("/api/posts/", format="json")
        self.assert_status_code(response, status.HTTP_200_OK)
        page_size = 20
        page_number = 1
        expected_posts_count = page_size * page_number
        assert len(response.data) <= expected_posts_count

    def test_retrieve_all_posts_with_custom_pagination_parameters(self):
        page_size = 10
        page_number = 2
        response = self.client.get(
            f"/api/posts/?page_size={page_size}&page_number={page_number}",
            format="json",
        )
        self.assert_status_code(response, status.HTTP_200_OK)
        expected_posts_count = page_size * page_number
        assert len(response.data) <= expected_posts_count
