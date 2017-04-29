# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
import json
from urllib import urlopen
from ..homeapp.models import Movies, GenreMovies, Genre
from suds.client import Client
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    context = Movies.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(context, 8)
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(paginator.num_pages)
    client = Client('http://soap.dev/server.php?wsdl')
    quantities = []
    for data in context:
        movie_quantity = client.service.getQuantity(data.id)
        temp = {'quantity': movie_quantity, 'id': data.id}
        quantities.append(temp)
    return render(request, 'homepage.html', {
        'data': movies,
        'homepage': True,
        'quantities': quantities
    })


def movie_details(request, movie_id):
    context = Movies.objects.get(pk=movie_id)
    client = Client('http://soap.dev/server.php?wsdl')
    movie_quantity = client.service.getQuantity(context.id)
    api = json.load(urlopen('https://api.themoviedb.org/3/movie/' + str(context.tmdb_id) + '?api_key=3a5fa430d771cb147fb889d04e147c3c'))
    api_videos = json.load(urlopen('https://api.themoviedb.org/3/movie/' + str(context.tmdb_id) + '/videos?api_key=3a5fa430d771cb147fb889d04e147c3c'))
    api_credits = json.load((urlopen('https://api.themoviedb.org/3/movie/' + str(context.tmdb_id) +'/credits?api_key=3a5fa430d771cb147fb889d04e147c3c')))
    return render(request, 'single_movie.html', {
        'movie': context,
        'movie_quantity': int(movie_quantity),
        'api': api,
        'video': api_videos,
        'credits': api_credits['cast']
    })


def movie_details_by_tmdb(request, tmdb_id):
    context = Movies.objects.get(tmdb_id=tmdb_id)
    client = Client('http://soap.dev/server.php?wsdl')
    movie_quantity = client.service.getQuantity(context.id)
    api = json.load(urlopen('https://api.themoviedb.org/3/movie/' + str(context.tmdb_id) + '?api_key=3a5fa430d771cb147fb889d04e147c3c'))
    api_videos = json.load(urlopen('https://api.themoviedb.org/3/movie/' + str(context.tmdb_id) + '/videos?api_key=3a5fa430d771cb147fb889d04e147c3c'))
    api_credits = json.load((urlopen('https://api.themoviedb.org/3/movie/' + str(context.tmdb_id) +'/credits?api_key=3a5fa430d771cb147fb889d04e147c3c')))
    return render(request, 'single_movie.html', {
        'movie': context,
        'api': api,
        'video': api_videos,
        'movie_quantity': int(movie_quantity),
        'credits': api_credits['cast']
    })


def movie_details_only_from_tmdb(request, tmdb_id):
    api = json.load(urlopen('https://api.themoviedb.org/3/movie/' + str(tmdb_id) + '?api_key=3a5fa430d771cb147fb889d04e147c3c'))
    api_videos = json.load(urlopen('https://api.themoviedb.org/3/movie/' + str(tmdb_id) + '/videos?api_key=3a5fa430d771cb147fb889d04e147c3c'))
    api_credits = json.load((urlopen('https://api.themoviedb.org/3/movie/' + str(tmdb_id) +'/credits?api_key=3a5fa430d771cb147fb889d04e147c3c')))
    return render(request, 'single_movie_tmdb.html', {
        'api': api,
        'video': api_videos,
        'credits': api_credits['cast']
    })


def get_movies_by_genre(request, genre_title):
    get_genre_id = Genre.objects.get(title__iexact=genre_title)
    genre_id = get_genre_id.id
    context = GenreMovies.objects.filter(genre_id=genre_id)
    page = request.GET.get('page', 1)
    paginator = Paginator(context, 8)
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(paginator.num_pages)
    client = Client('http://soap.dev/server.php?wsdl')
    quantities = []
    for data in context:
        movie_quantity = client.service.getQuantity(data.movie.id)
        temp = {'quantity': movie_quantity, 'id': data.movie.id}
        quantities.append(temp)
    return render(request, 'genre_movies.html', {
        'data': movies,
        'homepage': False,
        'quantities': quantities
    })


def search_movie_multi(request):
    query = request.GET.get('query', '')
    page = request.GET.get('page', '')
    if page is None or page == '' or page == 0:
        page = 1
    store_ids = Movies.objects.values_list('tmdb_id', flat=True)
    api = json.load(urlopen('https://api.themoviedb.org/3/search/multi?api_key=3a5fa430d771cb147fb889d04e147c3c&language=en-US&query='+str(query)+'&page='+str(page)))
    return render(request, 'multi_search.html', {
        'data': api,
        'homepage': False,
        'store_ids': store_ids,
        'keyword': query,
        'total_pages': range(api['total_pages']),
        'current_page': int(page)
    })


def search_movie_by_actor(request):
    query = request.GET.get('query', '')
    page = request.GET.get('page', '')
    if page is None or page == '' or page == 0:
        page = 1
    store_ids = Movies.objects.values_list('tmdb_id', flat=True)
    api = json.load(urlopen('https://api.themoviedb.org/3/search/person?api_key=3a5fa430d771cb147fb889d04e147c3c&search_type=ngram&query=' + str(query) + '&page='+str(page)))
    actor_id = api['results'][0]['id']
    info = json.load(urlopen('https://api.themoviedb.org/3/discover/movie?api_key=3a5fa430d771cb147fb889d04e147c3c&with_cast=' + str(actor_id)))
    return render(request, 'movies_actors.html', {
        'data': info,
        'actor_id': actor_id,
        'store_ids': store_ids,
        'homepage': False,
        'keyword': query,
        'total_pages': range(api['total_pages']),
        'current_page': int(page)
    })
