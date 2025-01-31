from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=255)
    year = models.CharField(max_length=4)
    rated = models.CharField(max_length=10)
    released = models.CharField(max_length=20)
    genre = models.CharField(max_length=255)
    actors = models.TextField()
    plot = models.TextField()
    meta = models.CharField(max_length=255)
    imdb = models.CharField(max_length=20)
    poster = models.URLField()

    def __str__(self):
        return self.title