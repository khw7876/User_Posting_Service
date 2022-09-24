from multiprocessing import managers
from post.serializers import PostSerializer
from post.models import HashTags as HashTagsModel, Post as PostModel

from user.models import User as UserModel

def create_post(create_data : dict[str, str], user : UserModel)-> None:
    hash_tag_data_list = create_data["hashtags"].replace(",", "").split("#")
    del hash_tag_data_list[0]
    create_data_hash_tag = []
    for hash_tag_data in hash_tag_data_list:
        HashTagsModel.objects.get_or_create(tags = hash_tag_data)
        create_data_hash_tag.append(HashTagsModel.objects.get(tags = hash_tag_data).id)
    create_data["hashtags"] = create_data_hash_tag
    create_data["user"] = user.id

    post_data_serializer = PostSerializer(data = create_data)
    post_data_serializer.is_valid(raise_exception=True)
    post_data_serializer.save()


def read_post():
    all_posts = PostModel.objects.all()
    post_serializer = PostSerializer(all_posts, many = True).data
    return post_serializer
    