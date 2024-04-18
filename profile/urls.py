from django.urls import path
from . import views


urlpatterns = [
    path('me/', views.me, name='profile'),
    path('', views.home, name='home'),
]
