from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.views.generic import CreateView
from .forms import CommentForm

# Create your views here.


class AddComment(CreateView):
    form_class = CommentForm

    def form_valid(self, form):
        content_type_id = self.request.POST.get("content_type_id")
        object_id = self.request.POST.get("object_id")

        content_type = get_object_or_404(ContentType, pk=content_type_id)
        obj = get_object_or_404(content_type.model_class(), pk=object_id)

        new_comment = form.save(commit=False)
        new_comment.author = self.request.user
        new_comment.content_object = obj
        new_comment.save()

    def get_success_url(self):
        return self.object.content_object.get_absolute_url()
