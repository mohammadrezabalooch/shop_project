from rest_framework import serializers
from .models import Product


class ProductSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "price",
            "stock",
            "category",
            "image",
            "id",
            # "comments",
        ]
