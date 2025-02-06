from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_movie, name='moviepage.search_movie'),
    path('movie/<movie_id>/', views.movie_detail, name='movie_detail'),
    path('<movie_id>/review/create/', views.create_review, name='moviepage.create_review'),
    path('<movie_id>/review/<int:review_id>/edit/', views.edit_review, name='moviepage.edit_review'),
    path('<movie_id>/review/<int:review_id>/delete/', views.delete_review, name='moviepage.delete_review'),
]

