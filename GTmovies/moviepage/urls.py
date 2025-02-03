from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_movie, name='moviepage.search_movie'),
    path('movie/<movie_id>/', views.movie_detail, name='movie_detail')
]

