from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Hashtag, Tag
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin


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

def hashtag_page(request, slug): #hashtag가 없으면 미분류로 hash태그가 없는 포스트만 보여줌.
    if slug == 'no_hashtag':
        hashtag = '미분류'
        post_list = Post.objects.filter(hashtag=None)
    else:
        hashtag = slug.objects.get(slug=slug)
        post_list = Post.objects.filter(hashtag=hashtag)

def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()

    return render(
        request,
        'index.html',
        {'post_list': post_list,
         'tag': tag,
         'hashtag': Hashtag.objects.all(),
         'no_hashtag_post_count': Post.objects.filter(hashtag=None).count()
         }
    )



class PostCreate(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title', 'content', 'head_image', 'hashtag', 'price']
    template_name = 'post_form.html'

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect('/post/')

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
