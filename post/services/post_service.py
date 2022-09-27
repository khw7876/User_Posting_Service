from post.serializers import PostSerializer
from post.models import HashTags as HashTagsModel, Like, Post as PostModel

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

def read_post(case:str):
    """
    게시글 목록을 보여주는 함수
    Args:
        case (str): "all, active 둘 중 하나로 모든 게시글, 활성화 게시글 분기"
    Returns:
        PostSerializer: post모델의 serializer
    """
    if case == all:
        posts_query_set = PostModel.objects.all()
    else:
        posts_query_set = PostModel.objects.filter(is_active = True)
    post_serializer = PostSerializer(posts_query_set, many = True).data
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

def delete_post(post_id : int)-> None:
    """
    게시글을 삭제(비활)하는 함수
    Args:
        post_id (int): "삭제할 게시글의 id"
    """
    delete_post_obj = PostModel.objects.get(id=post_id)
    delete_post_obj.is_active = False
    delete_post_obj.save()
    
def check_is_author(user : UserModel, post_id : int)-> bool:
    """
    로그인 한 유저가 해당 게시글의 작성자인지를 판단하는 함수
    Args:
        user (UserModel): "현재 로그인이 되어있는 User",
        post_id (int) : "권한을 체크할 게시글 id"

    Returns:
        bool: _description_
    """
    check_post_obj = PostModel.objects.get(id = post_id)
    if check_post_obj.user == user:
        return True
    return False

def recover_post(user : UserModel, post_id : int)-> None:
    """
    비활성화 되어있는 게시물을 다시 활성화 하는 함수
    Args:
        user (UserModel): "현재 로그인이 되어있는 User",
        post_id (int): "다시 활성화 할 게시글 id"
    """
    active_post_obj = PostModel.objects.get(id = post_id)
    active_post_obj.is_active = True
    active_post_obj.save()

def check_post_is_active(post_id : int):
    """
    게시글이 현재 활성화 상태인지 체크하는 로직
    Args:
        post_id (int): "활성화 여부를 체크할 게시글 id"

    Returns:
        True : "활성화 상태일 때",
        False : "비활성화 상태일 때" 
    """
    check_post_obj = PostModel.objects.get(id = post_id)
    if check_post_obj.is_active:
        return True
    return False

def like_post(post_id : int, user : UserModel):
    """
    게시글을 좋아요 또는 취소하는 기능

    Args:
        post_id (int): "좋아요를 할 게시글의 id"
    """
    post_obj = PostModel.objects.get(id=post_id)
    liked_post, created = Like.objects.get_or_create(post = post_obj, user = user)
    if created:
        return True
    liked_post.delete()
    return False

def get_detail_post(post_id : int):
    """
    게시글 상세보기 기능

    Args:
        post_id (int): "상세보기 할 게시글의 id"
    """
    post_obj = PostModel.objects.get(id=post_id)
    post_obj.views += 1
    post_obj.save()
    post_serializer = PostSerializer(post_obj).data
    return post_serializer


