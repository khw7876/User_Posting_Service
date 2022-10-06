from django.db.models import Count

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

def read_post_search(search : str)-> PostModel:
    """
    검색한 단어기반으로 PostModel을 찾는 함수
    Args:
        search (str): 검색할 단어를 결정하는 값,

    Returns:
        posts_query_set: 검색단어기반 검색을 마친 PostModel
    """

    posts_query_set = (PostModel.objects.filter(title__icontains = search)
    |
    PostModel.objects.filter(content__icontains = search))

    return posts_query_set

def read_post_order_by(posts_query_set : PostModel, reverse : int, order_by : str)-> PostModel:
    """
    정렬기준에 맞추어 PostModel을 정렬하는 함수
    Args:
        reverse (int): 내림차 or 오름차를 결정하는 값, 들어올 수 있는 값 = {0(내림차), 1(오름차)}, default = 0
        order_by (str): 정렬을 하기 위한 값, 들어올 수 있는 값 = {create_date, like, views}, default = created_at

    Returns:
        posts_query_set: 검색단어, 내림차, 정렬기준을 거친 PostModel
    """
    if reverse == 0:
        reverse = "-"
    elif reverse == 1:
        reverse = ""

    if (order_by == "create_date") or (order_by == "views"):
        posts_query_set = posts_query_set.order_by(reverse + order_by)
    elif order_by == "like":
        posts_query_set = posts_query_set.annotate(like_count = Count("like")).order_by(reverse + 'like_count')
    else:
        posts_query_set = posts_query_set.order_by("-create_date")
    return posts_query_set


def read_post_hashtags(posts_query_set : PostModel, hashtags : str):
    """
    해시태그를 통한 필터링을 거치는 함수
    Args:
        posts_query_set (PostModel): 검색단어, 내림차, 정렬기준을 거친 PostModel
        hashtags (str): 필터링 할 해시태그들

    Returns:
        PostModel: 검색단어, 내림차, 정렬기준, 해시태그 필터링을 거친 PostModel
    """

    hashtags = hashtags.split(",")

    hashtag_list = []
    for hashtag in hashtags:
        hashtag_list.append(HashTagsModel.objects.get(tags = hashtag))

    for a in hashtag_list:
        posts_query_set = posts_query_set.filter(hashtags__tags = a)
    return posts_query_set

def read_post_check_is_active(posts_query_set : PostModel, is_active : int):
    """
    게시물을 활성화 된 게시물만 가져올지, 전체를 가져올지 정제하는 함수
    Args:
        posts_query_set (PostModel): 검색단어, 내림차, 정렬기준, 해시태그 필터링을 거친 PostModel
        is_active (int): 게시글의 활성화 여부, 들어올 수 있는 값 = {0(활성화), 1(모든)}, default = 1

    Returns:
        PostModel: 검색단어, 내림차, 정렬기준, 해시태그 필터링, 활성화 여부체크를 거친 PostModel
    """
    if is_active == 0:
        posts_query_set = posts_query_set.filter(is_active = True)
    elif is_active == 1:
        posts_query_set = posts_query_set.all()
    return posts_query_set

def read_post_paginated(posts_query_set : PostModel, page : int, page_size : int):
    """
    필터링 된 PostModel을 페이지네이션 해주는 함수
    Args:
        page (int) : 현재 페이지의 위치, 들어올 수 있는 값 = int, default = 1,
        page_size (int) : 페이지당 게시글의 수, 들어올 수 있는 값 = int, default = 10,
    Returns:
        PostSerializer: post모델의 serializer
    """

    posts_query_set = posts_query_set[(page-1) * page_size : (page-1) * page_size + page_size]
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

def recover_post(post_id : int)-> None:
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


