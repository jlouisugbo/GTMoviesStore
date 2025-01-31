import requests
from django.shortcuts import render
from django.conf import settings
from urllib.parse import quote


def search_movie(request):

    if request.method == 'GET' and 'query' in request.GET:

        query = request.GET['query']
        api_key = settings.OMDB_API_KEY
        encoded_query = quote(query)
        url = f"http://www.omdbapi.com/?apikey={api_key}&t={encoded_query}"

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if data.get('Response') == 'True':
                return render(request, 'moviepage/movie_detail.html', {'movie': data})
            else:
                error_message = data.get('Error', 'Movie not found.')
                return render(request, 'moviepage/search.html', {'error': error_message})
        else:
            return render(request, 'moviepage/search.html', {'error': 'Failed to fetch data from the API.'})

    return render(request, 'moviepage/search.html')


def movie_detail(request):
    return render(request, 'moviepage/movie_detail.html')