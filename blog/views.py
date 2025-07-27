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
    model = Post
    template_name = "blog/post_list.html"


class PostDetailView(UserPassesTestMixin, DetailView):
    model = Post
    template_name = "blog/post_detail.html"

    # def test_func(self):
    #     obj = self.get_object()
    #     return obj.is_special and self.request.user.is_special


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ("title", "body")
    template_name = "blog/post_create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.status = "d"
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = "blog/post_update.html"
    fields = ("title", "body")

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class PostDeleteView(DeleteView):
    model = Post
    template_name = "blog/post_delete.html"
    success_url = reverse_lazy("postlist")
