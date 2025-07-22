from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Product
from django.urls import reverse_lazy

# Create your views here.


class ProductList(ListView):
    model = Product
    template_name = "products/product_list.html"


class ProductDetail(DeleteView):
    model = Product
    template_name = "products/product_Detail.html"


class ProductCreateView(CreateView):
    model = Product
    template_name = "products/product_create.html"
    fields = "__all__"


class ProductUpdateView(UpdateView):
    model = Product
    template_name = "products/product_update.html"
    fields = ("name", "price", "category", "description")


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "products/product_delete.html"
    success_url = reverse_lazy("productlist")
