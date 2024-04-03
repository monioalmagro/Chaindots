from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.user.models import User
from apps.user.serializer import UserSerializer


class UserDetailAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_post_count(user):
        return user.post_set.all().count()

    @staticmethod
    def get_comments_count(user):
        return user.comment_set.all().count()

    @staticmethod
    def get_followers(user):
        followers_users = user.followers.all()
        return UserSerializer(followers_users, many=True)

    @staticmethod
    def get_following(user):
        following_users = user.following.all()
        return UserSerializer(following_users, many=True)

    def get_user_data(self, user):
        posts_count = self.get_post_count(user)
        comments_count = self.get_comments_count(user)
        followers = self.get_followers(user)
        following = self.get_following(user)

        serializer = UserSerializer(user)
        user_data = serializer.data
        user_data["total_posts"] = posts_count
        user_data["total_comments"] = comments_count
        user_data["followers"] = followers.data
        user_data["following"] = following.data
        return user_data

    def get(self, request, user_id, format=None):
        try:
            user = User.objects.get(pk=user_id)

            user_data = self.get_user_data(user)

            return Response(user_data)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
