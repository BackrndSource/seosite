from rest_framework import serializers
from .models import Page, Image, Config


class SearchByExternalReferenceSerializer(serializers.Serializer):
    ext_ref = serializers.CharField()


class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Config
        fields = "__all__"


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"
