# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from decimal import Decimal


class Genre(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return "%s" % self.title


class Movies(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    year = models.CharField(max_length=10)
    cover = models.ImageField(upload_to='static/uploads/', default='static/uploads/no-img.png')
    tmdb_id = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return "%s - %s" % (self.title, self.year)


class GenreMovies(models.Model):
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return "%s | %s" % (self.movie.title, self.genre.title)