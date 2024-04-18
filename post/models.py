from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self): # 포스트제목 정의
        return f'[{self.pk}]{self.title}'

    def get_absolute_url(self): # get_absolute_url로 각 게시물로 가는 기능을 활성화
        return f'/post/{self.pk}/'
