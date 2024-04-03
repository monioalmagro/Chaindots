from django.core.exceptions import ObjectDoesNotExist

from apps.comment.models import Comment
from apps.comment.serializer import CommentSerializer
from apps.post import constants
from apps.post.models import Post
from apps.user.models import User


def get_user_and_post(author_id: int, post_id: int):
    """
    Get the user and post objects based on the provided author_id and post_id.

    Args:
        author_id (int): The ID of the author for the user object.
        post_id (int): The ID of the post for the post object.

    Returns:
        tuple: A tuple containing the user and post objects if found.

    Raises:
        AssertionError: If the user or post object is not found.
    """
    try:
        user = User.objects.get(pk=author_id)
        post = Post.objects.get(pk=post_id)
        return user, post
    except ObjectDoesNotExist as exp:
        raise AssertionError(constants.USER_OR_POST_NOT_FOUND) from exp


def create_comment(user: User, post: Post, content: str) -> Comment:
    comment = Comment(author=user, post=post, content=content)
    comment.save()
    return comment


def serializer_data(comment) -> CommentSerializer:
    return CommentSerializer(comment).data


def get_comments_by_post(post) -> CommentSerializer:
    comments = post.post_comment_set.all()
    return CommentSerializer(comments, many=True)
