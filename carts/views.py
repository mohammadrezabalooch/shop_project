from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Cart, CartItem
from products.models import Product

# Create your views here.


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product = get_object_or_404(Product, id=product_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, item=product)

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return redirect("productlist")


class RemoveFromCartView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        cart = get_object_or_404(Cart, user=request.user)
        product = get_object_or_404(Product, id=product_id)
        cart_item = CartItem.objects.get(cart=cart, item=product)
        if cart_item.quantity == 1:
            cart_item.delete()
        else:
            cart_item.quantity -= 1
            cart_item.save()
        return redirect("productlist")


class CartDetailView(LoginRequiredMixin, TemplateView):
    template_name = "carts/cart_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        context["cart"] = cart
        return context
