from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('update_post/<int:pk>/', views.PostUpdate.as_view()),
    path('create_post/', views.PostCreate.as_view()),
    path('tag/<str:slug>/', views.tag_page),
    path('hashtag/<str:slug>/', views.hashtag_page),
    path('<int:pk>/', views.PostDetail.as_view(), name='post-detail'),
    path('', views.PostList.as_view()), # 디폴트 페이지가 Postlist를 바로 보여주도록 수정
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('search/<str:q>/', views.PostSearch.as_view(), name='search'),
]
