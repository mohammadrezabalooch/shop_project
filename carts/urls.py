from django.urls import path
from .views import (
    AddToCartView,
    RemoveFromCartView,
    CartDetailView,
    CartDetailAPIView,
    CartAddAPIView,
    CartDeleteAPIView,
)

urlpatterns = [
    path("add/<int:product_id>/", AddToCartView.as_view(), name="cartadd"),
    path("remove/<int:product_id>/", RemoveFromCartView.as_view(), name="cartremove"),
    path("detail/", CartDetailView.as_view(), name="cartdetail"),
    #
    # api urls
    #
    path("api/detail/", CartDetailAPIView.as_view(), name="apicartdetail"),
    path("api/add/<int:pk>/", CartAddAPIView.as_view(), name="apicartadd"),
    path("api/delete/<int:pk>/", CartDeleteAPIView.as_view(), name="apicartdelete"),
]
