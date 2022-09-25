from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .services.post_service import(
    create_post,
    read_post,
    update_post,
    get_hashtags_list
)

# Create your views here.
class PostView(APIView):
    """
    post에 관련된 CRUD를 담당하는 View
    """
    def get(self, request: Request) -> Response:
        post_serializer = read_post()
        return Response(post_serializer, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        create_data = get_hashtags_list(request.data)
        create_post(create_data, request.user)
        return Response({"detail" : "게시글이 작성되었습니다."}, status=status.HTTP_200_OK)

    def put(self, request: Request, post_id: int)-> Response:
        update_post(request.data, post_id)
        return Response({"detail" : "게시글이 수정되었습니다."}, status=status.HTTP_200_OK)
        