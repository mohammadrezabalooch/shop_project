from django.urls import path
from .views import (
    ProductList,
    ProductDetail,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
)

urlpatterns = [
    path("", ProductList.as_view(), name="productlist"),
    path("<int:pk>/", ProductDetail.as_view(), name="productdetail"),
    path("add/", ProductCreateView.as_view(), name="productcreate"),
    path("edit/<int:pk>/", ProductUpdateView.as_view(), name="productupdate"),
    path("delete/<int:pk>", ProductDeleteView.as_view(), name="productdelete"),
]
