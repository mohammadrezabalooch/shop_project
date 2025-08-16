from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostPreviewView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    AuthorListView,
    PostListCreateAPIView,
    PostDetailAPIView,
    PostPreviewAPIView,
    AuthorListAPIView,
)

urlpatterns = [
    path("", PostListView.as_view(), name="postlist"),
    path("<int:pk>/", PostDetailView.as_view(), name="postdetail"),
    path("preview/<int:pk>/", PostPreviewView.as_view(), name="postpreview"),
    path("add/", PostCreateView.as_view(), name="postcreate"),
    path("edit/<int:pk>/", PostUpdateView.as_view(), name="postupdate"),
    path("delete/<int:pk>/", PostDeleteView.as_view(), name="postdelete"),
    path("author/<slug:username>/", AuthorListView.as_view(), name="authorlist"),
    #
    # api urls
    #
    path("api/", PostListCreateAPIView.as_view(), name="apipostlist"),
    path("api/<int:pk>/", PostDetailAPIView.as_view(), name="apipostdetail"),
    path("api/preview/<int:pk>/", PostPreviewAPIView.as_view(), name="apipostpreview"),
    path(
        "api/author/<slug:username>/", AuthorListAPIView.as_view(), name="apiauthorlist"
    ),
]
