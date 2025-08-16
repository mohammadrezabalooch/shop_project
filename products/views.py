from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Product
from django.urls import reverse_lazy
from comments.forms import CommentForm
from django.contrib.contenttypes.models import ContentType
from rest_framework import generics
from .serializers import ProductSerilizer
from rest_framework.permissions import IsAdminUser, AllowAny
from .permissions import IsAdminOrReadOnly

# Create your views here.


class ProductList(ListView):
    model = Product
    paginate_by = 6
    template_name = "products/product_list.html"


class ProductDetail(DetailView):
    model = Product
    template_name = "products/product_Detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context["comment_form"] = CommentForm()
        context["content_type_id"] = ContentType.objects.get_for_model(product).pk
        return context


class ProductCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Product
    template_name = "products/product_create.html"
    fields = "__all__"

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    template_name = "products/product_update.html"
    fields = ("name", "price", "category", "description", "image")

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = "products/product_delete.html"
    success_url = reverse_lazy("productlist")

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False


class ProductSearchView(ListView):
    template_name = "products/search_list.html"

    def get_queryset(self):
        search = self.request.GET.get("q")
        return Product.objects.filter(name__icontains=search)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["searchword"] = self.request.GET.get("q")
        return context


class ProductListAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerilizer
    permission_classes = [
        IsAdminOrReadOnly,
    ]


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerilizer
    permission_classes = [
        IsAdminOrReadOnly,
    ]


class ProductSearchAPIView(generics.ListAPIView):

    def get_queryset(self):
        search = self.request.GET.get("q")
        if search:
            return Product.objects.filter(name__icontains=search)
        return Product.objects.none()

    serializer_class = ProductSerilizer
    permission_classes = [
        AllowAny,
    ]
