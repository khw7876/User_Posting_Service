from rest_framework import serializers
from .models import HashTags as HashTagsModel, Like, Post as PostModel

class PostSerializer(serializers.ModelSerializer):
    hashtag_names = serializers.SerializerMethodField()

    def get_hashtag_names(self, obj):
        hash_tag_names = []
        for hash_tag_name in obj.hashtags.filter():
            hash_tag_names.append("#" + hash_tag_name.tags)
        return hash_tag_names

    class Meta:
        model = PostModel
        fields = ["id", "user", "title", "content", "hashtags", "hashtag_names", "is_active", "views", "create_date", "update_date"]
        extra_kwargs = {"hashtags": {"write_only": True}}

class DetailPostSerializer(serializers.ModelSerializer):
    hashtag_names = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()


    def get_hashtag_names(self, obj):
        hash_tag_names = []
        for hash_tag_name in obj.hashtags.filter():
            hash_tag_names.append("#" + hash_tag_name.tags)
        return hash_tag_names

    def get_like_count(self, obj):
        return Like.objects.filter(post=obj.id).count()

    class Meta:
        model = PostModel
        fields = ["id", "user", "title", "content", "hashtags", "hashtag_names", "is_active", "like_count", "views", "create_date", "update_date"]
        extra_kwargs = {"hashtags": {"write_only": True}}

