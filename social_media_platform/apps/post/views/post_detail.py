from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.comment.serializer import CommentSerializer
from apps.post import constants
from apps.post.models import Post
from apps.post.serializer import PostSerializer
from apps.user.serializer import UserSerializer


class PostDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get(self, request, id, format=None):
        try:
            post = Post.objects.get(pk=id)

            comments = post.post_comment_set.all().order_by("-created_at")[
                : constants.COMMENTS_BY_POST
            ]
            comments_serializer = CommentSerializer(comments, many=True)

            creator_serializer = UserSerializer(post.author)

            post_serializer = PostSerializer(post)

            data = {
                "post": post_serializer.data,
                "last_three_comments": comments_serializer.data,
                "creator": creator_serializer.data,
            }
            return Response(data)
        except Post.DoesNotExist:
            return Response(
                {"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )
