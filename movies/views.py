from django.shortcuts import render
from moviepage.models import Movie

movies = Movie.objects.filter(status__icontains = "Active").order_by("-year")[::]


def index(request):
    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html',
                  {'template_data': template_data})