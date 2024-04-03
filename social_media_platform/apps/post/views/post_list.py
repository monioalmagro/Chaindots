from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.post.models import Post
from apps.post.serializer import PostSerializer


class PostListCreateAPIView(APIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def filter_posts(self, request):
        posts = Post.objects.all()
        if author_id := request.query_params.get("author_id"):
            posts = posts.filter(author_id=author_id)

        from_date = request.query_params.get("from_date")
        to_date = request.query_params.get("to_date")
        if from_date and to_date:
            posts = posts.filter(created_at__range=[from_date, to_date])
        return posts.order_by("-created_at")

    def paginate_posts(self, request, posts):
        page_size = int(request.query_params.get("page_size", 20))
        page_number = int(request.query_params.get("page_number", 1))
        paginator = Paginator(posts, page_size)
        try:
            return paginator.page(page_number)
        except PageNotAnInteger:
            return paginator.page(1)
        except EmptyPage:
            return []

    def get(self, request, format=None):
        posts = self.filter_posts(request)
        paginated_posts = self.paginate_posts(request, posts)
        serializer = PostSerializer(paginated_posts, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
