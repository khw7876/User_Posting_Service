from rest_framework import status, permissions, exceptions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Post as PostModel
from .services.post_service import(
    create_post,
    read_post_paginated,
    update_post,
    delete_post,
    get_hashtags_list,
    check_is_author,
    recover_post,
    check_post_is_active,
    like_post,
    get_detail_post,
    read_post_search,
    read_post_order_by,
    read_post_hashtags,
    read_post_check_is_active
)

# Create your views here.
class PostView(APIView):
    """
    post에 관련된 CRUD를 담당하는 View
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def get(self, request: Request) -> Response:
        
        search = self.request.query_params.get("search", '')
        posts_query_set = read_post_search(search)

        reverse = int(self.request.query_params.get("reverse", 0))
        order_by = self.request.query_params.get("order_by", 'create_date')
        posts_query_set = read_post_order_by(posts_query_set, reverse, order_by)

        hashtags = self.request.query_params.get("hashtags", '')
        posts_query_set = read_post_hashtags(posts_query_set, hashtags)

        is_active = int(self.request.query_params.get("is_active", 1))
        posts_query_set = read_post_check_is_active(posts_query_set, is_active)

        page = int(self.request.query_params.get("page", 1))
        page_size = int(self.request.query_params.get("page_size", 10))
        post_serializer = read_post_paginated(posts_query_set, page, page_size)
        
        return Response(post_serializer, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        try:
            create_data = get_hashtags_list(request.data)
            create_post(create_data, request.user)
            return Response({"detail" : "게시글이 작성되었습니다."}, status=status.HTTP_201_CREATED)
        except exceptions.ValidationError as e:
                error_message = "".join([str(value) for values in e.detail.values() for value in values])
                return Response({"detail": error_message}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request: Request, post_id: int)-> Response:
        if check_is_author(request.user, post_id):
            try:
                update_data = get_hashtags_list(request.data)
                update_post(update_data, post_id)
                return Response({"detail" : "게시글이 수정되었습니다."}, status=status.HTTP_201_CREATED)
            except PostModel.DoesNotExist:
                return Response({"detail" : "수정할 게시글이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"detail" : "게시글의 수정은 작성자만이 할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)

    def delete(slef, request: Request, post_id: int)-> Response:
        if check_is_author(request.user, post_id):
            try:
                delete_post(post_id)
                return Response({"detail" : "게시글이 삭제(비활) 되었습니다."}, status=status.HTTP_200_OK)
            except PostModel.DoesNotExist:
                return Response({"detail" : "삭제하려는 게시글이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"detail" : "게시글의 삭제는 작성자만이 할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)
        
class RecoverPostView(APIView):
    """
    비활성화 된 post를 다시 활성화 시켜주는 View
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def put(slef, request: Request, post_id: int):
        if check_post_is_active(post_id):
            return Response({"detail" : "게시글이 활성화가 되어있는 상태입니다."}, status=status.HTTP_400_BAD_REQUEST)
        recover_post(post_id)
        return Response({"detail" : "게시글이 복구되었습니다."}, status=status.HTTP_200_OK)

class LikeView(APIView):
    """
    게시글을 좋아요 하는 View
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def post(self, request: Request, post_id: int):
        if like_post(post_id, request.user):
            return Response({"detail" : "게시글이 좋아요 되었습니다."}, status=status.HTTP_200_OK)
        return Response({"detail" : "게시글이 좋아요가 취소 되었습니다."}, status=status.HTTP_200_OK)

class DetialPostView(APIView):
    """
    게시글을 상세보기 하는 Views
    """
    def get(self, request: Request, post_id: int):
        detail_post_serializer = get_detail_post(post_id)
        return Response(detail_post_serializer, status=status.HTTP_200_OK)