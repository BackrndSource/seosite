from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product, ProductImage, Review
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ProductImageSerializer,
    ProductExternalUpdateSerializer,
    ReviewSerializer,
    SearchByExternalReferenceSerializer,
)
from django.views.generic import ListView, DetailView
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

# from rest_framework.parsers import MultiPartParser, FormParser
from django.http import HttpResponse
from django.views.decorators.http import require_GET
import os


# Website Views
class HomeView(ListView):
    model = Category
    queryset = Category.objects.filter(parent=None)


class ProductListView(ListView):
    model = Category
    queryset = Product.objects.filter(visible=True)
    template_name = "giftos/product/views/list.html"


class ProductDetailView(DetailView):
    context_object_name = "product"
    queryset = Product.objects.filter(visible=True)
    template_name = "giftos/product/views/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["shop_categories"] = Category.objects.filter(visible=True, parent=None)
        context["canonical_url_base"] = os.getenv("CANONICAL_URL_BASE")
        return context


class CategoryListView(ListView):
    model = Category
    queryset = Category.objects.filter(visible=True)
    template_name = "giftos/category/views/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["shop_categories"] = Category.objects.filter(visible=True, parent=None)
        context["canonical_url_base"] = os.getenv("CANONICAL_URL_BASE")

        return context


class CategoryDetailView(DetailView):
    context_object_name = "category"
    queryset = Category.objects.all()
    template_name = "giftos/category/views/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add 'product reviews' in selected 'category' to the view context
        # SQLiteDB doesnt have Distinct lookup implementation, then we do manually.
        # products = Product.objects.filter(categories__in=[self.get_object()])
        products = self.get_object().products.filter(visible=True)
        reviews = []
        for product in products:
            latest_obj = (
                Review.objects.filter(product=product, product__visible=True).order_by("-rating").first()
            )  # Get only the best rated review per product in category
            if latest_obj:
                reviews.append(latest_obj)
        context["reviews"] = reviews

        # Disctint lookup for DB supporting it
        # context["reviews"] = Review.objects.filter(
        #     product__in=Product.objects.filter(
        #         categories__in=[self.get_object()]
        #     )
        # ).order_by("-rating").distinct("product")

        context["featured_products"] = products.filter(featured=True).order_by(
            "-last_modified", "-rating_count", "-rating"
        )
        context["promo_products"] = products.filter(real_price__isnull=False).order_by(
            "-last_modified", "-rating_count", "-rating"
        )
        context["bestselling_products"] = products.filter(rating__gte=4).order_by(
            "-rating_count", "-last_modified", "-rating"
        )
        context["bestrated_products"] = products.filter(rating__gte=4).order_by(
            "-rating", "-rating_count", "-last_modified"
        )

        context["shop_categories"] = Category.objects.filter(visible=True, parent=None)

        context["canonical_url_base"] = os.getenv("CANONICAL_URL_BASE")

        return context


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ["title", "product__ext_ref"]
    filterset_fields = "__all__"
    ordering_fields = "__all__"
    ordering = ["-last_modified"]
    permission_classes = [IsAuthenticated]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ["title", "ext_ref"]
    filterset_fields = ["parent", "featured", "visible"]
    ordering_fields = "__all__"
    ordering = ["-last_modified"]
    permission_classes = [IsAuthenticated]
    # parser_classes = [MultiPartParser, FormParser]

    # def create(self, request, *args, **kwargs):
    #     image = request.data["image"]
    #     return super().create(request, *args, **kwargs)

    @action(detail=False, methods=["post"], serializer_class=SearchByExternalReferenceSerializer)
    def search_ext_ref(self, request):
        if "ext_ref" in request.data:
            category = Category.objects.get(ext_ref=request.data["ext_ref"])
            return Response(CategorySerializer(category).data) if category else Response()
        return Response()


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ["title", "ext_ref"]
    filterset_fields = "__all__"
    ordering_fields = "__all__"
    ordering = ["-last_modified"]
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["post"], serializer_class=SearchByExternalReferenceSerializer)
    def search_ext_ref(self, request):
        if "ext_ref" in request.data:
            product = Product.objects.get(ext_ref=request.data["ext_ref"])
            return Response(CategorySerializer(product).data) if product else Response()
        return Response()

    @action(detail=False, methods=["post"], serializer_class=ProductExternalUpdateSerializer)
    def external_update(self, request):
        if "products" in request.data:
            products_created = []
            products_updated = []
            products_errored = []

            images_created = []
            images_updated = []
            images_errored = []

            reviews_created = []
            reviews_updated = []
            reviews_errored = []

            def update_or_create_images(images, product):
                position = 0
                for image in images:
                    image["position"] = position  # Maybe better in client
                    image["product"] = product
                    try:
                        _image, created = ProductImage.objects.update_or_create(small=image["small"], defaults=image)
                        position += 1
                        images_created.append(
                            ProductImageSerializer(_image).data
                        ) if created else images_updated.append(ProductImageSerializer(_image).data)
                    except Exception as e:
                        del image["product"]
                        images_errored.append(image.pk)

            def update_or_create_reviews(reviews, product):
                for review in reviews:
                    review["product"] = product  # Maybe better in client
                    try:
                        _review, created = Review.objects.update_or_create(
                            product=product, text=review["text"], defaults=review
                        )
                        reviews_created.append(ReviewSerializer(_review).data) if created else reviews_updated.append(
                            ReviewSerializer(_review).data
                        )
                    except Exception as e:
                        del review["product"]
                        reviews_errored.append(review)

            def add_categories(categories, product):
                try:
                    product.categories.set(categories)
                    product.save()
                except Exception as e:
                    pass

            for product in request.data["products"]:
                if "asin" in product:
                    categories = []
                    images = []
                    reviews = []
                    if "categories" in product:
                        categories = product["categories"]
                        del product["categories"]
                    if "images" in product:
                        images = product["images"]
                        del product["images"]
                    if "reviews" in product:
                        reviews = product["reviews"]
                        del product["reviews"]

                    replace_product = request.data["replace_product"] if ("replace_product" in request.data) else False

                    try:
                        if replace_product:
                            # Replace product
                            _product, created = Product.objects.update_or_create(asin=product["asin"], defaults=product)
                            products_created.append(
                                ProductSerializer(_product).data
                            ) if created else products_updated.append(ProductSerializer(_product).data)
                        else:
                            # Create product
                            _product = Product.objects.create(**product)
                            products_created.append(ProductSerializer(_product).data)
                        if categories:
                            add_categories(categories, _product)
                        if images:
                            update_or_create_images(images, _product)
                        if reviews:
                            update_or_create_reviews(reviews, _product)
                    except Exception as e:
                        update_product = request.data["update_product"] if ("update_product" in request.data) else False
                        if update_product:
                            # Update product
                            update_price = request.data["update_price"] if ("update_price" in request.data) else False
                            update_rating = (
                                request.data["update_rating"] if ("update_rating" in request.data) else False
                            )
                            update_description = (
                                request.data["update_description"] if ("update_description" in request.data) else False
                            )
                            update_images = (
                                request.data["update_images"] if ("update_images" in request.data) else False
                            )
                            update_reviews = (
                                request.data["update_reviews"] if ("update_reviews" in request.data) else False
                            )
                            update_categories = (
                                request.data["update_categories"] if ("update_categories" in request.data) else False
                            )

                            defaults = {"asin": product["asin"], "slug": product["asin"]}  # TODO create the slug

                            if update_price:
                                if "price" in product:
                                    defaults["price"] = product["price"]
                                if "real_price" in product:
                                    defaults["real_price"] = product["real_price"]

                            if update_rating:
                                if "rating" in product:
                                    defaults["rating"] = product["rating"]
                                if "rating_count" in product:
                                    defaults["rating_count"] = product["rating_count"]

                            if update_description:
                                if "description" in product:
                                    defaults["description"] = product["description"]

                            try:
                                _product, created = Product.objects.update_or_create(
                                    asin=product["asin"], defaults=defaults
                                )

                                products_updated.append(ProductSerializer(_product).data)

                                if categories and update_categories:
                                    add_categories(categories, _product)

                                if images and update_images:
                                    update_or_create_images(images, _product)

                                if reviews and update_reviews:
                                    update_or_create_reviews(reviews, _product)

                            except Exception as e:
                                products_errored.append(product)
                        else:
                            products_errored.append(product)

        return Response(
            {
                "products_created": products_created,
                "products_updated": products_updated,
                "products_errored": products_errored,
                "images_created": images_created,
                "images_updated": images_updated,
                "images_errored": images_errored,
                "reviews_created": reviews_created,
                "reviews_updated": reviews_updated,
                "reviews_errored": reviews_errored,
            }
        )


class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ["product__title", "product__ext_ref"]
    filterset_fields = "__all__"
    ordering_fields = "__all__"
    ordering = ["-last_modified"]
    permission_classes = [IsAuthenticated]


@require_GET
def robots_txt(request):
    robots_txt_content = f"""
    User-agent: *
    Disallow:

    Sitemap: {request.build_absolute_uri('/sitemap.xml')}
    """
    return HttpResponse(robots_txt_content, content_type="text/plain")
