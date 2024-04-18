from django.shortcuts import render
from .models import Post


# Create your views here.
def index(request):
    posts = Post.objects.all().order_by('-pk') # DB에 쿼리를 날려 원하는 레코드 가져오기, orderby로 최신 포스트(personal_key의 역순)로 정렬.

    return render(request, 'index.html',
                   {
                      'posts': posts
                     }
                  )

def single_post_page(request, pk):
    post = Post.objects.get(pk=pk)

    return render(
        request,
        'single_post_page.html',
        {
            'post': post,
        }
    )
