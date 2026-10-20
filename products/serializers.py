import os
from urllib.parse import quote

from django.conf import settings
from rest_framework import serializers
from .models import Product, Image


class ImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ["id", "image_url", "product"]

    def get_image_url(self, obj):
        stored_path = str(obj.image_url or "").replace("\\", "/")
        if stored_path.startswith(("http://", "https://", "data:")):
            return stored_path

        filename = os.path.basename(stored_path)
        if not filename:
            return ""

        return (
            f"{settings.MEDIA_URL.rstrip('/')}/product_images/"
            f"{obj.product_id}/{quote(filename)}"
        )


class ProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "name", "price", "subcategory", "subcategories", "images"]

    def get_subcategories(self, obj):
        return list(obj.subcategory.values_list("name", flat=True))
