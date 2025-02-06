import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from urllib.parse import quote
from django.contrib.auth.decorators import login_required
from .models import Movie, Review

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, imdb_id=movie_id)
    reviews = Review.objects.filter(movie=movie)
    return render(request, 'moviepage/movie_detail.html', {'movie': movie, 'reviews': reviews})

def search_movie(request):
    search = 'moviepage/search.html'
    if request.method == 'GET' and 'query' in request.GET:

        query = request.GET['query']
        api_key = settings.OMDB_API_KEY
        encoded_query = quote(query)
        url = f"https://www.omdbapi.com/?apikey={api_key}&s={encoded_query}&type=movie"
        search = 'moviepage/search.html'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get('Response') == 'True':
                movies = [m for m in data.get("Search", []) if m.get("Type") == "movie"]
                add_movies(movies,query)
                movies = Movie.objects.filter(title__icontains=query).order_by('title').distinct()
                return render(request, search, {'movies': movies})
            else:
                error_message = data.get('Error', 'Movie not found.')
                return render(request, search, {'error': error_message})
        else:
            return render(request, search, {'error': 'Failed to fetch data from the API.'})

    return render(request, search)

'''
The add_movies function is used to add movies to the database. 
It takes the request, a list of movies, and a query as arguments. 
It iterates over the list of movies and checks if the query is present in the movie title. 
If the query is present and the movie is not already in the database, it makes a request to the OMDB API to get detailed information about the movie.
It then creates a Movie object with the information from the API response and saves it to the database.
'''
def add_movies(movies,query):
    for item in movies:
        if query.lower() in item['Title'].lower() and not (Movie.objects.filter(imdb_id=item['imdbID']).exists()) and \
                item['Poster'] != 'N/A':
            api_key = settings.OMDB_API_KEY
            url = f"https://www.omdbapi.com/?apikey={api_key}&i={item['imdbID']}"
            response = requests.get(url)
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
        else:
            continue

@login_required
def create_review(request, movie_id):
    movie = get_object_or_404(Movie, imdb_id=movie_id)
    reviews = Review.objects.filter(movie=movie)
    if request.method == 'POST' and request.POST['comment'] != '':
        movie = get_object_or_404(Movie, imdb_id=movie_id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.imdb_id = movie.imdb_id
        review.save()
        return render(request, 'moviepage/movie_detail.html', {'movie': movie, 'reviews': reviews})
    else:
        movie = get_object_or_404(Movie, imdb_id=movie_id)
        return render(request, 'moviepage/movie_detail.html', {'movie': movie, 'reviews': reviews})

@login_required
def edit_review(request, movie_id, review_id):
   review = get_object_or_404(Review, id=review_id)
   movie = get_object_or_404(Movie, imdb_id=movie_id)
   reviews = Review.objects.filter(movie=movie)
   if request.user != review.user:
       return render(request, 'moviepage/movie_detail.html', {'movie': movie, 'reviews': reviews})
   if request.method == 'GET':
       template_data = {}
       template_data['title'] = 'Edit Review'
       template_data['review'] = review
       return render(request, 'moviepage/edit_review.html',{'template_data': template_data})
   elif request.method == 'POST' and request.POST['comment'] != '':
       review = Review.objects.get(id=review_id)
       review.comment = request.POST['comment'] + ' (edited)'
       review.save()
       return render(request, 'moviepage/movie_detail.html', {'movie': movie, 'reviews': reviews})
   else:
       return render(request, 'moviepage/movie_detail.html', {'movie': movie, 'reviews': reviews})


@login_required
def delete_review(request, movie_id, review_id):
   movie = get_object_or_404(Movie, imdb_id=movie_id)
   reviews = Review.objects.filter(movie=movie)
   review = get_object_or_404(Review, id=review_id, user=request.user)
   review.delete()
   return render(request, 'moviepage/movie_detail.html', {'movie': movie, 'reviews': reviews})