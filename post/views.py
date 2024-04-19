from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Hashtag, Tag
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
from django.db.models import Q

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

        def form_valid(self, form):
            current_user = self.request.user
            if current_user.is_authenticated:
                form.instance.author = current_user
                response = super(PostCreate, self).form_valid(form)

                tags_str = self.request.POST.get('tags_str')
                if tags_str:
                    tags_str = tags_str.strip()

                    tags_str = tags_str.split(',',';')
                    tags_list = tags_str.split(';')

                    for t in tags_list:
                        t = t.strip()
                        tag, is_tag_created = Tag.objects.get_or_create(name=t)
                        if is_tag_created:
                            tag.slug = slugify(t, allow_unicode=True)
                            tag.save()
                        self.object.tags.add(tag)

                return response



class PostUpdate(LoginRequiredMixin,UpdateView):
    model = Post
    fields = ['title', 'content', 'head_image', 'hashtag', 'price']

    template_name = 'post_update_form.html'

    def get_context_data(self, **kwargs):
        context = super(PostUpdate, self).get_context_data()
        if self.object.tags.exists():
            tags_str_list = list()
            for t in self.object.tags.all():
                tags_str_list.append(t.name)
            context['tags_str_default'] = ';'.join(tags_str_list)

        return context

    def form_valid(self, form):
        response = super(PostUpdate, self).form_valid(form)
        self.object.tags.clear()

        tags_str = self.request.POST.get('tags_str')
        if tags_str:
            tags_str = tags_str.strip()
            tags_str = tags_str.split(',',';')
            tags_list = tags_str.split(';')

            for t in tags_list:
                t = t.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name=t)
                if is_tag_created:
                    tag.slug = slugify(t, allow_unicode=True)
                    tag.save()
                self.object.tags.add(tag)

        return response

    def dispatch(self, request, *args, **kwargs): # 작성자만 수정가능
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied #권한없음

def login_view(request):
    return render(request, 'login.html')

def signup_view(request):
    return render(request, 'signup.html')


class PostSearch(PostList):
    paginate_by = None

    def get_queryset(self):
        q = self.kwargs['q']
        post_list = Post.objects.filter(title__icontains=q).distinct()
        return post_list

    def get_context_data(self, **kwargs):
        context = super(PostSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search: {q} ({self.get_queryset().count()})'

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
