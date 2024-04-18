from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.

class Hashtag(models.Model):
    name = models.CharField(max_length=50, unique=True) #unique로 같은 해시태그를 다시 달 수 없도록 함.
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True) #unicode로 한국어 입력지원도 도움.

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Hashtags' #복수형이라 이름변경

class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    head_image = models.ImageField(upload_to='post/images/%Y/%m/%d/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL) # on_delete = 이 포스트의 작성자가 db에서 삭제됐을때 이 포스트도 함께 삭제함.
    hashtag = models.ForeignKey(Hashtag, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self): # 포스트제목 정의
        return f'[{self.pk}]{self.title} :: {self.author}' # 작성자도 출력되도록 함.

    def get_absolute_url(self): # get_absolute_url로 각 게시물로 가는 기능을 활성화
        return f'/post/{self.pk}/'


# 상세 날짜폴더까지 타고 들어가는건 시간에 큰 영향을 주지않지만 한 폴더안에 너무 많은 파일이 있다면 파일을 찾는데 오래걸림.
