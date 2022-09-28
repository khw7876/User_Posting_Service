from django.test import TestCase

from user.models import User as UserModel

class TestPostService(TestCase):
    """
    Post의 서비스 함수들을 검증하는 클래스
    """

    @classmethod
    def setUpClassData(cls):
        user = UserModel.objects.create(username="ko", nickname="ko")