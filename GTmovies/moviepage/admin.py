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
        Custom view to refresh movies (e.g., fetch from an external API).
        """
        api_key = settings.OMDB_API_KEY
        search_terms = ["Inception", "Interstellar", "The Dark Knight", "Pulp Fiction", "Fight Club"]

        added_count = 0
        updated_count = 0

        for title in search_terms:
            url = f"https://www.omdbapi.com/?apikey={api_key}&t={title}"
            response = requests.get(url)

            if response.status_code == 200:
                movie_data = response.json()

                if movie_data.get('Response') == 'True':
                    imdb_id = movie_data.get('imdbID')
                    movie_obj, created = Movie.objects.update_or_create(
                        imdb_id=imdb_id,
                        defaults={
                            'title': movie_data.get('Title', 'Unknown'),
                            'year': movie_data.get('Year'),
                            'rated': movie_data.get('Rated'),
                            'released': movie_data.get('Released'),
                            'runtime': movie_data.get('Runtime'),
                            'genre': movie_data.get('Genre'),
                            'director': movie_data.get('Director'),
                            'writer': movie_data.get('Writer'),
                            'actors': movie_data.get('Actors'),
                            'plot': movie_data.get('Plot'),
                            'language': movie_data.get('Language'),
                            'country': movie_data.get('Country'),
                            'awards': movie_data.get('Awards'),
                            'poster': movie_data.get('Poster'),
                            'imdb_rating': movie_data['imdbRating'] if movie_data['imdbRating'] != 'N/A' else None,
                        }
                    )
                    if created:
                        added_count += 1
                    else:
                        updated_count += 1

        self.message_user(
            request,
            f"Movies refreshed successfully! {added_count} added, {updated_count} updated.",
            messages.SUCCESS
        )

        return redirect('..')
