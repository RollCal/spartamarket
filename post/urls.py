from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.single_post_page, name='single_post_page'),
    # path('', views.index, name='index'),
    path('', views.PostList.as_view()), # 디폴트 페이지가 Postlist를 바로 보여주도록 수정
]
