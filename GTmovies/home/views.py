from django.shortcuts import render
from moviepage.models import Movie
import random

def index(request):
    movies = Movie.objects.all()
    randomized_movies = random.sample(list(movies), len(movies))  # Shuffle the list

    context = {
        'movies': randomized_movies
    }
    return render(request, 'home/index.html', context)

def about(request):
    template_data = {}
    template_data['title'] = 'About'
    return render(request, 'home/about.html', {'template_data': template_data})
