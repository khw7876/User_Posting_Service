from django.test import TestCase
from rest_framework import exceptions

from post.models import Post as PostModel, HashTags as HashTagsModel
from user.models import User as UserModel
from post.services.post_service import(
    get_hashtags_list,
    create_post,
    read_post_search,
    read_post_order_by,
    update_post,
)

DOES_NOT_EXIST_NUM = 0

class TestPostService(TestCase):
    """
    Post의 서비스 함수들을 검증하는 클래스
    """

    @classmethod
    def setUpTestData(cls):
        user = UserModel.objects.create(username="ko", email="ko@naver.com")
        hashtags = HashTagsModel.objects.create(tags = "해시태그")
        post = PostModel.objects.create(user = user, title = "게시글 제목", content = "게시글 내용")
        post.hashtags_tags = hashtags
    def test_when_success_get_hashtags_list(self)-> None:
        """
        "#"과 ","이 들어있는 해시태그를 사용할 수 있는 형태로 변환해주는 함수에 대한 검증
        case : 성공적으로 분리가 되었을 경우
        result : 리스트형태로 태그들의 id 저장
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

    def test_when_None_tags_geted_in_get_hashtags_list(self) -> None:
        """
        "#"과 ","이 들어있는 해시태그를 사용할 수 있는 형태로 변환해주는 함수에 대한 검증
        case : 비어있는 해시태그를 넣어주었을 경우
        result : 비어있는 상태로 실행
        """
        request_data = {"hashtags" : ""}
        hash_tag_data = {}
        hash_tag_data_list = request_data["hashtags"].replace(",", "").split("#")
        hash_tag_data["hashtags"] = []
        self.assertEqual(hash_tag_data, get_hashtags_list(request_data))

    def test_when_None_Sharp_in_get_hashtags_list(self)-> None:
        """
        "#"과 ","이 들어있는 해시태그를 사용할 수 있는 형태로 변환해주는 함수에 대한 검증
        case : #이 없는 형태로 들어왔을 경우
        result : 해당 덩어리 자체로 저장
        """
        request_data = {"hashtags" : "태그1,태그2"}
        hash_tag_data = {}
        hash_tag_data_list = request_data["hashtags"].replace(",", "").split("#")
        del hash_tag_data_list[0]
        request_data_hash_tag = []
        for hash_tag in hash_tag_data_list:
            HashTagsModel.objects.get_or_create(tags = hash_tag)
            request_data_hash_tag.append(HashTagsModel.objects.get(tags = hash_tag).id)
        hash_tag_data["hashtags"] = request_data_hash_tag

        self.assertEqual(hash_tag_data, get_hashtags_list(request_data))

    def test_when_success_create_post(self):
        """
        게시글을 생성하는 함수에 대한 검증
        case : 정상적으로 게시물이 생성이 되었을 경우
        result : 전체의 게시물 개수가 함수가 실행되고 1개 늘어남
        """
        user = UserModel.objects.get(username="ko", email="ko@naver.com")
        tags_tags = HashTagsModel.objects.get(tags = "해시태그")

        request_data = {
            "title" : "게시글 제목",
            "content" : "게시글 내용", 
            "hashtags" : [tags_tags.id]}

        count1 = PostModel.objects.all().count()
        create_post(request_data, user)
        count2 = PostModel.objects.all().count()
        
        self.assertEqual(count1 + 1, count2)
    
    def test_when_None_title_in_create_post(self):
        """
        게시글을 생성하는 함수에 대한 검증
        case : title에 비어있는 값을 넣었을 경우
        result : validation을 통과하지 못하고 ValidationError 반환
        """
        user = UserModel.objects.get(username="ko", email="ko@naver.com")
        tags_tags = HashTagsModel.objects.get(tags = "해시태그")

        request_data = {
            "title" : "",
            "content" : "게시글 내용", 
            "hashtags" : [tags_tags.id]}
        
        with self.assertRaises(exceptions.ValidationError):
            create_post(request_data, user)

    def test_when_None_content_in_create_post(self):
        """
        게시글을 생성하는 함수에 대한 검증
        case : content에 비어있는 값을 넣었을 경우
        result : validation을 통과하지 못하고 ValidationError 반환
        """
        user = UserModel.objects.get(username="ko", email="ko@naver.com")
        tags_tags = HashTagsModel.objects.get(tags = "해시태그")

        request_data = {
            "title" : "게시글 제목",
            "content" : "", 
            "hashtags" : [tags_tags.id]}
        
        with self.assertRaises(exceptions.ValidationError):
            create_post(request_data, user)

    def test_when_None_content_in_create_post(self):
        """
        게시글을 생성하는 함수에 대한 검증
        case : content에 비어있는 값을 넣었을 경우
        result : validation을 통과하지 못하고 ValidationError 반환
        """
        user = UserModel.objects.get(username="ko", email="ko@naver.com")
        tags_tags = HashTagsModel.objects.get(tags = "해시태그")

        request_data = {
            "title" : "게시글 제목",
            "content" : "", 
            "hashtags" : [tags_tags.id]}
        
        with self.assertRaises(exceptions.ValidationError):
            create_post(request_data, user)

    def test_when_success_read_post_search(self):
        """
        게시글을 제목, 내용에 포함된 단어로 검색을 하는 함수 검증
        case : 검색이라는 단어가 포함된 게시글 2개 생성, 검색
        result : 검색이라는 단어가 포함된 게시글 2개 검색됨
        """
        user = UserModel.objects.get(username="ko", email="ko@naver.com")
        PostModel.objects.create(title = "검색1", content = "검색1", user = user)
        PostModel.objects.create(title = "검색2", content = "검색2", user = user)
        read_post_search("검색")
        self.assertEqual(2, read_post_search("검색").count())

    def test_when_getted_wrong_order_by_in_read_post_order_by(self):
        read_post_order_by(PostModel.objects.all(), reverse = 1, order_by="zzz")

    def test_when_success_update_post(self):
        """
        게시글을 수정하는 함수에 대한 검증
        case : 정상적으로 게시물이 수정이 되었을 경우
        result : 게시글이 수정이 되었음
        """
        
        update_post_obj = PostModel.objects.get(title = "게시글 제목", content = "게시글 내용")

        update_data = {
            "title" : "게시글 제목",
            "content" : "게시글 내용"}

        update_post(update_data, update_post_obj.id)
        self.assertEqual(update_post_obj.title, update_data["title"])

    def test_when_does_not_exist_post_in_update_post(self):
        """
        게시글을 수정하는 함수에 대한 검증
        case : 수정하려는 게시글이 존재하지 않을 경우
        result : 404에러 Does_not_exist Error 발생
        """
        update_data = {
            "title" : "게시글 제목",
            "content" : "게시글 내용"}

        with self.assertRaises(PostModel.DoesNotExist):
            update_post(update_data, DOES_NOT_EXIST_NUM)

    def test_when_title_or_content_under_4length_in_update_post(self):
        """
        게시글을 수정하는 함수에 대한 검증
        case : title에 4글자 이하로 데이터를 넣었을 경우
        result : Serializer의 validateion을 통과하지 못하고 Validation 에러 발생
        """
        update_post_obj = PostModel.objects.get(title = "게시글 제목", content = "게시글 내용")

        update_data = {
            "title" : "에러",
            "content" : "게시글 내용"}

        with self.assertRaises(exceptions.ValidationError):
            update_post(update_data, update_post_obj.id)

    def test_when_None_title_or_content_in_update_post(self):
        """
        게시글을 수정하는 함수에 대한 검증
        case : 필수적인 요소인 title이나 content가 들어가지 않았을 경우
        result : Serializer의 validateion을 통과하지 못하고 Validation 에러 발생
        """
        update_post_obj = PostModel.objects.get(title = "게시글 제목", content = "게시글 내용")

        update_data = {
            "content" : "게시글 내용"}

        with self.assertRaises(exceptions.ValidationError):
            update_post(update_data, update_post_obj.id)
