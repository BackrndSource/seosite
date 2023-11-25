from .models import Page, Image, Config
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import PageSerializer, ImageSerializer, ConfigSerializer, SearchByExternalReferenceSerializer
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser


class ConfigViewSet(viewsets.ModelViewSet):
    queryset = Config.objects.all()
    serializer_class = ConfigSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = "__all__"
    ordering_fields = "__all__"
    permission_classes = [IsAuthenticated]


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = "__all__"
    ordering_fields = "__all__"
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]


class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ["title", "ext_ref"]
    filterset_fields = ["parent", "featured", "visible"]
    ordering_fields = "__all__"
    ordering = ["-last_modified"]
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["post"], serializer_class=SearchByExternalReferenceSerializer)
    def search_ext_ref(self, request):
        if "ext_ref" in request.data:
            page = Page.objects.get(ext_ref=request.data["ext_ref"])
            return Response(PageSerializer(page).data) if page else Response()
        return Response()

    def list(self, request, *args, **kwargs):
        if request.query_params.get("all", False):
            self.pagination_class = None
        return super().list(request, *args, **kwargs)
