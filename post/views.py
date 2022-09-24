from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .services.post_service import(
    create_post,
)

# Create your views here.
class PostView(APIView):
    """
    post에 관련된 CRUD를 담당하는 View
    """
    def post(self, request: Request) -> Response:
        create_post(request.data)
        return Response()
        