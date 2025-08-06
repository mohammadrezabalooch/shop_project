from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Post
from django.db.models import Q
from django.contrib.auth import get_user_model
from comments.forms import CommentForm
from django.contrib.contenttypes.models import ContentType

# Create your views here.


class PostListView(ListView):
    # model = Post
    paginate_by = 3
    template_name = "blog/post_list.html"
    queryset = Post.objects.filter(status="p")


class PostDetailView(UserPassesTestMixin, DetailView):
    template_name = "blog/post_detail.html"
    queryset = Post.objects.filter(status="p")

    def test_func(self):
        obj = self.get_object()
        if obj.is_special:
            return (
                self.request.user.is_special_user() or self.request.user == obj.author
            )
        return True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context["comment_form"] = CommentForm()
        context["content_type_id"] = ContentType.objects.get_for_model(post).pk
        return context


class PostPreviewView(UserPassesTestMixin, DetailView):
    # model = Post
    template_name = "blog/post_detail.html"
    queryset = Post.objects.filter(Q(status="d") | Q(status="b"))

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ("title", "body", "is_special")
    template_name = "blog/post_create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.status = "d"
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_author


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = "blog/post_update.html"
    fields = ("title", "body", "image")

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_delete.html"
    success_url = reverse_lazy("postlist")

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class AuthorListView(ListView):
    template_name = "blog/author.html"
    paginate_by = 3

    def get_queryset(self):
        username = self.kwargs.get("username")
        author = get_object_or_404(get_user_model(), username=username)

        return author.articles.filter(status="p")

    context_object_name = "authorposts"
