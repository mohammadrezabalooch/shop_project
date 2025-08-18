from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Cart, CartItem
from products.models import Product
from .serializers import CartSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response

# Create your views here.


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product = get_object_or_404(Product, id=product_id)
        # میشه اینجا شرط گذاشت موجودی کالا چک بشه اما چون موجودی کالا عددی مثبته هرموقع صفر باشه و کاربر ادد کنه خودش ارور میده پس بهینه نیست برای اون حالت خاص هربار یه شرط بررسی بشه
        cart_item, created = CartItem.objects.get_or_create(cart=cart, item=product)

        if not created:
            cart_item.quantity += 1
            # product.stock -= 1  #با signal نوشتم خودکار از موجودی کم میشه
            # product.save()
            cart_item.save()
        # else:
        #     product.stock -= 1
        #     product.save()
        next_url = request.POST.get("next", "productlist")
        return redirect(next_url)


class RemoveFromCartView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        cart = get_object_or_404(Cart, user=request.user)
        product = get_object_or_404(Product, id=product_id)
        cart_item = CartItem.objects.get(cart=cart, item=product)
        if cart_item.quantity == 1:
            cart_item.delete()
        else:
            cart_item.quantity -= 1
            # product.stock += 1  #با signals نوشتم خودکار به تعداد موجود محصول اضافه میکنه
            # product.save()
            cart_item.save()

        next_url = request.POST.get("next", "productlist")
        return redirect(next_url)


class CartDetailView(LoginRequiredMixin, TemplateView):
    template_name = "carts/cart_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        context["cart"] = cart
        return context


class CartDetailAPIView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart


class CartAddAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer
    queryset = Product.objects.all()

    def post(self, request, pk, *args, **kwargs):
        item = self.get_object()
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        serializer = self.get_serializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartDeleteAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer
    queryset = Product.objects.all()

    def post(self, request, pk, *args, **kwargs):
        item = self.get_object()
        cart = get_object_or_404(Cart, user=self.request.user)
        cart_item = CartItem.objects.get(cart=cart, item=item)

        if cart_item.quantity == 1:
            cart_item.delete()
        else:
            cart_item.quantity -= 1
            cart_item.save()

        serializer = self.get_serializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)
