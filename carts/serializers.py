from rest_framework import serializers
from .models import Cart, CartItem
from products.serializers import ProductSerilizer


class CartItemSerializer(serializers.ModelSerializer):
    item = ProductSerilizer(read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "item", "quantity"]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only="True")

    class Meta:
        model = Cart
        fields = ["user", "id", "items"]
