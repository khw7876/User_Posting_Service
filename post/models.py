from django.db import models

from user.models import User
# Create your models here.

class HashTags(models.Model):
    tags = models.CharField("해시태그", max_length=20)

    def __str__(self):
        return self.tags

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField("제목", max_length=50)
    content = models.CharField("내용", max_length=500)
    hashtags = models.ManyToManyField(HashTags, blank=True)
    is_active = models.BooleanField("활성화", default=True)
    views = models.PositiveSmallIntegerField("조회수", default=0)
    create_date = models.DateTimeField("작성일", auto_now_add=True)
    update_date = models.DateTimeField("수정일", auto_now=True)

    def __str__(self):
        return self.user, self.title

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.user, self.post


    
