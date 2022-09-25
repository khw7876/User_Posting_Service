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
    get_hashtags_list
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
        return Response({"detail" : "게시글이 작성되었습니다."}, status=status.HTTP_200_OK)

    def put(self, request: Request, post_id: int)-> Response:
        update_data = get_hashtags_list(request.data)
        update_post(update_data, post_id)
        return Response({"detail" : "게시글이 수정되었습니다."}, status=status.HTTP_200_OK)

    def delete(slef, request: Request, post_id: int)-> Response:
        delete_post(post_id)
        return Response({"detail" : "게시글이 삭제(비활) 되었습니다."}, status=status.HTTP_200_OK)
        