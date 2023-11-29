from .models import Category, Post, Image, Comment, Config
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import (
    CategorySerializer,
    PostSerializer,
    ImageSerializer,
    CommentSerializer,
    SearchByExternalReferenceSerializer,
)
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = "__all__"
    ordering_fields = "__all__"
    ordering = ["-last_modified"]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        image = request.data["image"]
        return super().create(request, *args, **kwargs)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ["title", "ext_ref"]
    filterset_fields = ["parent", "featured", "visible"]
    ordering_fields = "__all__"
    ordering = ["-last_modified"]
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["post"], serializer_class=SearchByExternalReferenceSerializer)
    def search_ext_ref(self, request):
        if "ext_ref" in request.data:
            category = Category.objects.get(ext_ref=request.data["ext_ref"])
            return Response(CategorySerializer(category).data) if category else Response()
        return Response()

    def list(self, request, *args, **kwargs):
        if request.query_params.get("all", False):
            self.pagination_class = None
        return super().list(request, *args, **kwargs)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.prefetch_related("images", "comments")
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ["title", "ext_ref"]
    filterset_fields = ["categories", "featured", "visible"]
    ordering_fields = "__all__"
    ordering = ["-last_modified"]
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["post"], serializer_class=SearchByExternalReferenceSerializer)
    def search_ext_ref(self, request):
        if "ext_ref" in request.data:
            post = Post.objects.get(ext_ref=request.data["ext_ref"])
            return Response(PostSerializer(post).data) if post else Response()
        return Response()


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ["title", "post__title", "post__ext_ref"]
    filterset_fields = "__all__"
    ordering_fields = "__all__"
    ordering = ["-last_modified"]
    permission_classes = [IsAuthenticated]
