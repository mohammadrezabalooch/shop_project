from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "title",
            "body",
            "status",
            "author",
            "is_special",
            "created_at",
            "updated_at",
            "image",
            # "comments",
        ]
