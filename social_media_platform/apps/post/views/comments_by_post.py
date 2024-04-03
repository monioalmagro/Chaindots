from pydantic import ValidationError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.comment.schema import CommentCreateSchema
from apps.post.models import Post
from apps.post.serializer import PostSerializer
from apps.post.utils import (
    create_comment,
    get_comments_by_post,
    get_user_and_post,
    serializer_data,
)


class CommentListAPIView(APIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, id, format=None):
        try:
            post = Post.objects.get(pk=id)

            comments = get_comments_by_post(post)

            post_serializer = PostSerializer(post)

            response_data = post_serializer.data
            response_data["comments"] = comments.data

            return Response(response_data)
        except Post.DoesNotExist:
            return Response(
                {"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def post(self, request, id, format=None):
        try:
            data = request.data
            comment_data = CommentCreateSchema(**data)

            user, post = get_user_and_post(comment_data.author_id, id)

            comment = create_comment(user, post, comment_data.comment)

            return Response(serializer_data(comment), status=201)

        except ValidationError as error:
            return Response({"error": error.errors()}, status=400)
        except AssertionError as error:
            return Response({"error": str(error)}, status=400)
