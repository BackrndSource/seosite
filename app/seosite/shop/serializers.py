from rest_framework import serializers
from .models import Category, Product, ProductImage, Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class CategoryPrimaryKeyRelatedSerializer(serializers.PrimaryKeyRelatedField, serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class SearchByExternalReferenceSerializer(serializers.Serializer):
    ext_ref = serializers.CharField()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductExternalUpdateSerializer(serializers.Serializer):
    asin = serializers.CharField()
    price = serializers.FloatField()
    real_price = serializers.FloatField()
    rating = serializers.FloatField()
    rating_count = serializers.IntegerField()
    categories = CategoryPrimaryKeyRelatedSerializer(many=True, queryset=Category.objects.all())


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"
