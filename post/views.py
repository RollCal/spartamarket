from django.views.generic import ListView, DetailView
from .models import Post, Hashtag


class PostList(ListView): # CBV
    model = Post
    template_name = 'index.html' # 이걸 안적으면 post_list.html을 템플릿으로 인식해버림
    ordering = '-pk' # 최신순 정렬

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['hashtags'] = Hashtag.objects.all()
        context['no_hashtag_post_count'] = Post.objects.filter(hashtag=None).count()
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['hashtags'] = Hashtag.objects.all()
        context['no_hashtag_post_count'] = Post.objects.filter(hashtag=None).count()
        return context



# Create your views here.
# def index(request):
#     posts = Post.objects.all().order_by('-pk') # DB에 쿼리를 날려 원하는 레코드 가져오기, orderby로 최신 포스트(personal_key의 역순)로 정렬.
#
#     return render(request, 'index.html',
#                    {
#                       'posts': posts
#                      }
#                   )
#
# def single_post_page(request, pk):
#     post = Post.objects.get(pk=pk)
#
#     return render(
#         request,
#         'post_detail.html',
#         {
#             'post': post,
#         }
#     )
