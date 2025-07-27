from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
)

urlpatterns = [
    path("", PostListView.as_view(), name="postlist"),
    path("<int:pk>/", PostDetailView.as_view(), name="postdetail"),
    path("add/", PostCreateView.as_view(), name="postcreate"),
    path("edit/<int:pk>/", PostUpdateView.as_view(), name="postupdate"),
    path("delete/<int:pk>", PostDeleteView.as_view(), name="postdelete"),
]
