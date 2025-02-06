from django.urls import path
from django.shortcuts import redirect
from django.contrib import admin, messages
from .models import Movie
import requests
from django.conf import settings


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'genre', 'created_at', 'updated_at')
    search_fields = ('title', 'year', 'genre')
    list_filter = ('year', 'genre')
    ordering = ('-created_at',)


    actions = ['mark_as_archived']
    change_list_template = 'admin/movies/movie/change_list.html'

    fieldsets = (
        (None, {
            'fields': ('title', 'year', 'rated', 'released', 'runtime', 'genre', 'director', 'writer', 'actors', 'plot')
        }),
        ('Additional Information', {
            'fields': ('language', 'country', 'awards', 'poster', 'imdb_rating', 'imdb_id', 'status'),
            'classes': ('collapse',),
        }),
    )

    def mark_as_archived(self, request, queryset):
        """
        Custom admin action to mark selected movies as archived.
        """
        queryset.update(status='archived')
        self.message_user(request, f"{queryset.count()} movies were marked as archived.", messages.SUCCESS)

    mark_as_archived.short_description = 'Mark selected movies as archived'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('refresh-movies/', self.admin_site.admin_view(self.refresh_movies), name='refresh_movies'),
        ]
        return custom_urls + urls

    def refresh_movies(self, request):
        """
        Refresh all movies in the database by fetching the latest data from the API.
        """
        api_key = settings.OMDB_API_KEY
        movies = Movie.objects.all()

        added_count = 0
        updated_count = 0

        for movie in movies:
            url = f"https://www.omdbapi.com/?apikey={api_key}&i={movie.imdb_id}"
            response = requests.get(url)

            if response.status_code == 200:
                movie_data = response.json()

                if movie_data.get('Response') == 'True':
                    movie.title = movie_data.get('Title', movie.title)
                    movie.year = movie_data.get('Year', movie.year)
                    movie.rated = movie_data.get('Rated', movie.rated)
                    movie.released = movie_data.get('Released', movie.released)
                    movie.runtime = movie_data.get('Runtime', movie.runtime)
                    movie.genre = movie_data.get('Genre', movie.genre)
                    movie.director = movie_data.get('Director', movie.director)
                    movie.writer = movie_data.get('Writer', movie.writer)
                    movie.actors = movie_data.get('Actors', movie.actors)
                    movie.plot = movie_data.get('Plot', movie.plot)
                    movie.language = movie_data.get('Language', movie.language)
                    movie.country = movie_data.get('Country', movie.country)
                    movie.awards = movie_data.get('Awards', movie.awards)
                    movie.poster = movie_data.get('Poster', movie.poster)
                    movie.imdb_rating = movie_data['imdbRating'] if movie_data['imdbRating'] != 'N/A' else None

                    movie.save()
                    updated_count += 1

        self.message_user(
            request,
            f"Movies refreshed successfully! {updated_count} updated.",
            messages.SUCCESS
        )

        return redirect('..')

