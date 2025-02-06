from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    title = models.CharField(max_length=255)
    year = models.CharField(max_length=4, null=True)
    rated = models.CharField(max_length=10, blank=True, null=True)
    released = models.CharField(max_length=20, blank=True, null=True)
    runtime = models.CharField(max_length=20, blank=True, null=True)
    genre = models.CharField(max_length=255, blank=True, null=True)
    director = models.CharField(max_length=255, blank=True, null=True)
    writer = models.CharField(max_length=255, blank=True, null=True)
    actors = models.TextField(blank=True, null=True)
    plot = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    awards = models.TextField(blank=True, null=True)
    poster = models.URLField(blank=True, null=True)
    imdb_rating = models.CharField(max_length=5, blank=True, null=True)
    imdb_id = models.CharField(max_length=20, unique=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True)

    status = models.CharField(
        max_length=50,
        choices=[('active', 'Active'), ('archived', 'Archived')],
        default='active'
    )

    def __str__(self):
        return self.title

class Review(models.Model):
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.movie.title + ' ' + self.user.username)