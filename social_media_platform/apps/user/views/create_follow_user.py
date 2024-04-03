from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.user.models import User


class UserCreateFollowAPIView(APIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, follower_id, followee_id, format=None):
        follower = get_object_or_404(User, pk=follower_id)
        followee = get_object_or_404(User, pk=followee_id)

        if follower == followee:
            return Response(
                {"error": "Cannot follow yourself"}, status.HTTP_400_BAD_REQUEST
            )

        if follower.following.filter(pk=followee_id).exists():
            return Response(
                {"error": "Already following this user"}, status.HTTP_400_BAD_REQUEST
            )

        follower.following.add(followee)
        return Response({"message": "You are now following this user"})
