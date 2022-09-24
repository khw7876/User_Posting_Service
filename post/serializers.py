from rest_framework import serializers
from .models import HashTags as HashTagsModel, Post as PostModel

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostModel
        fields = ["id", "title", "content", "hashtags", "is_active", "views", "create_date", "update_date"]

