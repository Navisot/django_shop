# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from cart.cart import Cart
import json
from urllib import urlopen
from ..homeapp.models import Movies, GenreMovies
from suds.client import Client
from suds.cache import NoCache


def index(request):
    current_cart = Cart(request)
    myCart = Cart.get_cart_details(current_cart)
    context = Movies.objects.all()
    return render(request, 'homepage.html', {
        'data': context,
        'homepage': True,
        'total_items': myCart['total_items'],
        'total_price': myCart['total_price'],
    })


def movie_details(request, movie_id):
    current_cart = Cart(request)
    myCart = Cart.get_cart_details(current_cart)
    context = Movies.objects.get(pk=movie_id)
    client = Client('http://soap.dev/server.php?wsdl', cache=NoCache())
    movie_quantity = client.service.getQuantity(context.id)
    api = json.load(urlopen('https://api.themoviedb.org/3/movie/' + str(context.tmdb_id) + '?api_key=3a5fa430d771cb147fb889d04e147c3c'))
    api_videos = json.load(urlopen('https://api.themoviedb.org/3/movie/' + str(context.tmdb_id) + '/videos?api_key=3a5fa430d771cb147fb889d04e147c3c'))
    return render(request, 'single_movie.html', {
        'movie': context,
        'movie_quantity': int(movie_quantity),
        'total_items': myCart['total_items'],
        'total_price': myCart['total_price'],
        'api': api,
        'video': api_videos,
    })


def movie_details_by_tmdb(request, tmdb_id):
    current_cart = Cart(request)
    myCart = Cart.get_cart_details(current_cart)
    context = Movies.objects.get(tmdb_id=tmdb_id)
    api = json.load(urlopen('https://api.themoviedb.org/3/movie/' + str(context.tmdb_id) + '?api_key=3a5fa430d771cb147fb889d04e147c3c'))
    api_videos = json.load(urlopen('https://api.themoviedb.org/3/movie/' + str(context.tmdb_id) + '/videos?api_key=3a5fa430d771cb147fb889d04e147c3c'))
    return render(request, 'single_movie.html', {
        'movie': context,
        'total_items': myCart['total_items'],
        'total_price': myCart['total_price'],
        'api': api,
        'video': api_videos,
    })


def movie_details_only_from_tmdb(request, tmdb_id):
    current_cart = Cart(request)
    myCart = Cart.get_cart_details(current_cart)
    api = json.load(urlopen(
        'https://api.themoviedb.org/3/movie/' + str(tmdb_id) + '?api_key=3a5fa430d771cb147fb889d04e147c3c'))
    api_videos = json.load(urlopen('https://api.themoviedb.org/3/movie/' + str(tmdb_id) + '/videos?api_key=3a5fa430d771cb147fb889d04e147c3c'))
    return render(request, 'single_movie_tmdb.html', {
        'total_items': myCart['total_items'],
        'total_price': myCart['total_price'],
        'api': api,
        'video': api_videos,
    })


def get_movies_by_genre(request, genre_id):
    current_cart = Cart(request)
    myCart = Cart.get_cart_details(current_cart)
    context = GenreMovies.objects.filter(genre_id=genre_id)
    return render(request, 'genre_movies.html', {
        'data': context,
        'homepage': False,
        'total_items': myCart['total_items'],
        'total_price': myCart['total_price'],
    })


def search_movie_multi(request):
    query = request.GET.get('query', '')
    current_cart = Cart(request)
    myCart = Cart.get_cart_details(current_cart)
    store_ids = Movies.objects.values_list('tmdb_id', flat=True)
    api = json.load(urlopen('https://api.themoviedb.org/3/search/multi?api_key=3a5fa430d771cb147fb889d04e147c3c&language=en-US&query='+str(query)+''))
    return render(request, 'multi_search.html', {
        'data': api,
        'homepage': False,
        'total_items': myCart['total_items'],
        'total_price': myCart['total_price'],
        'store_ids': store_ids,
        'keyword': query
    })

