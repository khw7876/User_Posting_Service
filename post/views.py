from rest_framework import status, permissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .services.post_service import(
    create_post,
    read_post,
    update_post,
    delete_post,
    get_hashtags_list,
    check_is_author,
    recover_post,
    check_post_is_active,
    like_post
)

# Create your views here.
class PostView(APIView):
    """
    post에 관련된 CRUD를 담당하는 View
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def get(self, request: Request, case: str) -> Response:
        post_serializer = read_post(case)
        return Response(post_serializer, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        create_data = get_hashtags_list(request.data)
        create_post(create_data, request.user)
        return Response({"detail" : "게시글이 작성되었습니다."}, status=status.HTTP_201_CREATED)

    def put(self, request: Request, post_id: int)-> Response:
        if check_is_author(request.user, post_id):
            update_data = get_hashtags_list(request.data)
            update_post(update_data, post_id)
            return Response({"detail" : "게시글이 수정되었습니다."}, status=status.HTTP_201_CREATED)
        return Response({"detail" : "게시글의 수정은 작성자만이 할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)

    def delete(slef, request: Request, post_id: int)-> Response:
        if check_is_author(request.user, post_id):
            delete_post(post_id)
            return Response({"detail" : "게시글이 삭제(비활) 되었습니다."}, status=status.HTTP_200_OK)
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
        recover_post(request.user, post_id)
        return Response({"detail" : "게시글이 복구되었습니다."}, status=status.HTTP_200_OK)

class LikeView(APIView):
    """
    게시글을 좋아요 하는 View
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def post(self, request: Request, post_id: int):
        like_post(post_id, request.user)
        return Response({"detail" : "게시글이 좋아요 되었습니다."}, status=status.HTTP_200_OK)