from post.serializers import PostSerializer
from post.models import HashTags as HashTagsModel, Post as PostModel

from user.models import User as UserModel


def get_hashtags_list(request_data : dict[str,str]):
    """
    #으로 받은 해시태그를 분리해서 다시 넣어주는 함수
    Args:
        request_data (dict[str,str]): {
            ```,
            "hashtags" : "게시글에 들어갈 해시태그, ex) #내용",
            ```
        }

    Returns:
        ```,
        "hashtags" : "게시글에 들어갈 해시태그, ex) 내용",
        ```
    """
    hash_tag_data_list = request_data["hashtags"].replace(",", "").split("#")
    del hash_tag_data_list[0]
    request_data_hash_tag = []
    for hash_tag_data in hash_tag_data_list:
        HashTagsModel.objects.get_or_create(tags = hash_tag_data)
        request_data_hash_tag.append(HashTagsModel.objects.get(tags = hash_tag_data).id)
    request_data["hashtags"] = request_data_hash_tag
    return request_data


def create_post(create_data : dict[str, str], user : UserModel)-> None:
    """
    게시글을 생성하는 함수
    Args:
        create_data (dict[str, str]): {
            "title" : "게시글의 제목",
            "content" : "게시글의 내용",
            "hashtags" : "게시글에 달을 해시태그"
        }
        user (UserModel): 현재 로그인이 되어있는 user object
    """
    create_data["user"] = user.id

    post_data_serializer = PostSerializer(data = create_data)
    post_data_serializer.is_valid(raise_exception=True)
    post_data_serializer.save()

def read_post():
    """
    게시글 목록을 보여주는 함수
    Returns:
        PostSerializer: post모델의 serializer
    """
    all_posts = PostModel.objects.all()
    post_serializer = PostSerializer(all_posts, many = True).data
    return post_serializer
    
def update_post(update_data : dict[str, str], post_id : int)-> None:
    """
    게시글을 수정하는 함수
    Args:
        update_data (dict[str, str]): {
            "title" : "게시글의 제목",
            "content" : "게시글의 내용",
            "hashtags" : "게시글에 달을 해시태그"
        }
        post_id (int): "수정할 게시글의 id"
    """
    update_post_obj = PostModel.objects.get(id=post_id)
    post_data_serializer = PostSerializer(update_post_obj, update_data, partial = True)
    post_data_serializer.is_valid(raise_exception=True)
    post_data_serializer.save()
    