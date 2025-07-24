from django.urls import path
from .views import AddToCartView, RemoveFromCartView, CartDetailView

urlpatterns = [
    path("add/<int:product_id>/", AddToCartView.as_view(), name="cartadd"),
    path("remove/<int:product_id>/", RemoveFromCartView.as_view(), name="cartremove"),
    path("detail/", CartDetailView.as_view(), name="cartdetail"),
]
