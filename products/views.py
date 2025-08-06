from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Product
from django.urls import reverse_lazy
from comments.forms import CommentForm
from django.contrib.contenttypes.models import ContentType

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


class ProductSearchView(ListView):
    template_name = "products/search_list.html"

    def get_queryset(self):
        search = self.request.GET.get("q")
        return Product.objects.filter(name__icontains=search)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["searchword"] = self.request.GET.get("q")
        return context
