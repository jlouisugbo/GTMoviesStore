from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_movie, name='moviepage.search_movie'),
    path('movie/', views.movie_detail, name='moviepage.movie_detail'),
]