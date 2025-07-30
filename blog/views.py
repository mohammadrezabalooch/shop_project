from django.shortcuts import render
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

# Create your views here.


class PostListView(ListView):
    # model = Post
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
    fields = ("title", "body")

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
