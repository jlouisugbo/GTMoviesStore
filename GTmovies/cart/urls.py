from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='cart.index'),
    path('<str:id>/add/', views.add, name='cart.add'),
    path('clear/', views.clear, name='cart.clear'),
     path('<str:id>/remove/', views.remove, name='cart.remove'),
]