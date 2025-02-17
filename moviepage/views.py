import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from urllib.parse import quote
from django.contrib.auth.decorators import login_required
from .models import Movie, Review

def movie_detail(request, movie_id):
    try:
        movie = get_object_or_404(Movie, imdb_id=movie_id)
        reviews = Review.objects.filter(movie=movie)
    except Exception as e:
        return render(request, 'moviepage/movie_detail.html', {'error': f"An error occurred: {str(e)}"})
    return render(request, 'moviepage/movie_detail.html', {'movie': movie, 'reviews': reviews})

def search_movie(request):
    search = 'moviepage/search.html'
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET['query']
        api_key = settings.OMDB_API_KEY
        encoded_query = quote(query)
        url = f"https://www.omdbapi.com/?apikey={api_key}&s={encoded_query}&type=movie"
        search = 'moviepage/search.html'

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raise an error for bad HTTP responses
        except requests.exceptions.Timeout:
            return render(request, search, {'error': 'Request timed out. Please try again later.'})
        except requests.exceptions.RequestException as e:
            return render(request, search, {'error': f"API request failed: {str(e)}"})

        if response.status_code == 200:
            data = response.json()
            if data.get('Response') == 'True':
                movies = [m for m in data.get("Search", []) if m.get("Type") == "movie"]
                add_movies(movies, query)
                movies = Movie.objects.filter(title__icontains=query).order_by('title').distinct()
                return render(request, search, {'movies': movies})
            else:
                error_message = data.get('Error', 'Movie not found.')
                return render(request, search, {'error': error_message})
        else:
            return render(request, search, {'error': 'Failed to fetch data from the API.'})

    return render(request, search)

def add_movies(movies, query):
    for item in movies:
        if query.lower() in item['Title'].lower() and not (Movie.objects.filter(imdb_id=item['imdbID']).exists()) and \
                item['Poster'] != 'N/A':
            api_key = settings.OMDB_API_KEY
            url = f"https://www.omdbapi.com/?apikey={api_key}&i={item['imdbID']}"
            try:
                response = requests.get(url)
                response.raise_for_status()  # Raise error for bad response
                movie = response.json()
                imdb = movie.get('imdbID')
                if not Movie.objects.filter(imdb_id=imdb).exists():
                    movie_obj = Movie.objects.create(
                        title=movie.get('Title', 'Unknown'),
                        year=movie.get('Year', None),
                        rated=movie.get('Rated', None),
                        released=movie.get('Released', None),
                        runtime=movie.get('Runtime', None),
                        genre=movie.get('Genre', None),
                        director=movie.get('Director', None),
                        writer=movie.get('Writer', None),
                        actors=movie.get('Actors', None),
                        plot=movie.get('Plot', None),
                        language=movie.get('Language', None),
                        country=movie.get('Country', None),
                        awards=movie.get('Awards', None),
                        poster=movie.get('Poster', None),
                        imdb_rating=movie['imdbRating'] if movie['imdbRating'] != 'N/A' else None,
                        imdb_id=movie.get('imdbID', None)
                    )
                    movie_obj.save()
            except requests.exceptions.RequestException as e:
                print(f"Error fetching movie details: {str(e)}")
                continue
        else:
            continue

@login_required
def create_review(request, movie_id):
    try:
        movie = get_object_or_404(Movie, imdb_id=movie_id)
        reviews = Review.objects.filter(movie=movie)
    except Exception as e:
        return render(request, 'moviepage/movie_detail.html', {'error': f"An error occurred: {str(e)}"})
    
    if request.method == 'POST' and request.POST['comment'] != '':
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.imdb_id = movie.imdb_id
        review.save()
        return render(request, 'moviepage/movie_detail.html', {'movie': movie, 'reviews': reviews})
    return render(request, 'moviepage/movie_detail.html', {'movie': movie, 'reviews': reviews})

@login_required
def edit_review(request, movie_id, review_id):
    try:
        review = get_object_or_404(Review, id=review_id)
        movie = get_object_or_404(Movie, imdb_id=movie_id)
        reviews = Review.objects.filter(movie=movie)
    except Exception as e:
        return render(request, 'moviepage/movie_detail.html', {'error': f"An error occurred: {str(e)}"})
    
    if request.user != review.user:
        return render(request, 'moviepage/movie_detail.html', {'movie': movie, 'reviews': reviews})
    if request.method == 'GET':
        template_data = {'title': 'Edit Review', 'review': review}
        return render(request, 'moviepage/edit_review.html', {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review.comment = request.POST['comment'] + ' (edited)'
        review.save()
        return render(request, 'moviepage/movie_detail.html', {'movie': movie, 'reviews': reviews})
    return render(request, 'moviepage/movie_detail.html', {'movie': movie, 'reviews': reviews})

@login_required
def delete_review(request, movie_id, review_id):
    try:
        movie = get_object_or_404(Movie, imdb_id=movie_id)
        reviews = Review.objects.filter(movie=movie)
        review = get_object_or_404(Review, id=review_id, user=request.user)
        review.delete()
    except Exception as e:
        return render(request, 'moviepage/movie_detail.html', {'error': f"An error occurred: {str(e)}"})
    return render(request, 'moviepage/movie_detail.html', {'movie': movie, 'reviews': reviews})
