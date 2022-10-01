from django.test import TestCase
from post.models import Post as PostModel, HashTags as HashTagsModel

from user.models import User as UserModel
from post.services.post_service import(
    get_hashtags_list,
)

class TestPostService(TestCase):
    """
    Post의 서비스 함수들을 검증하는 클래스
    """

    @classmethod
    def setUpClassData(cls):
        user = UserModel.objects.create(username="ko", nickname="ko")
        hashtags = HashTagsModel.objects.create(tags = "해시태그")
        post = PostModel.objects.create(user = user, title = "게시글 제목", content = "게시글 내용", hashtags = hashtags)

    def test_when_success_get_hashtags_list(self)-> None:
        """
        "#"과 ","이 들어있는 해시태그를 사용할 수 있는 형태로 변환해주는 함수에 대한 검증
        case : 성공적으로 분리가 되었을 경우
        """
        request_data = {"hashtags" : "#태그1,#태그2"}
        hash_tag_data = {}
        hash_tag_data_list = request_data["hashtags"].replace(",", "").split("#")
        del hash_tag_data_list[0]
        request_data_hash_tag = []
        for hash_tag in hash_tag_data_list:
            HashTagsModel.objects.get_or_create(tags = hash_tag)
            request_data_hash_tag.append(HashTagsModel.objects.get(tags = hash_tag).id)
        hash_tag_data["hashtags"] = request_data_hash_tag

        self.assertEqual(hash_tag_data, get_hashtags_list(request_data))

