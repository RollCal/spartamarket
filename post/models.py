from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    head_image = models.ImageField(upload_to='post/images/%Y/%m/%d/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL) # on_delete = 이 포스트의 작성자가 db에서 삭제됐을때 이 포스트도 함께 삭제함.

    def __str__(self): # 포스트제목 정의
        return f'[{self.pk}]{self.title} :: {self.author}' # 작성자도 출력되도록 함.

    def get_absolute_url(self): # get_absolute_url로 각 게시물로 가는 기능을 활성화
        return f'/post/{self.pk}/'


# 상세 날짜폴더까지 타고 들어가는건 시간에 큰 영향을 주지않지만 한 폴더안에 너무 많은 파일이 있다면 파일을 찾는데 오래걸림.
