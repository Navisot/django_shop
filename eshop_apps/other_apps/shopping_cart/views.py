# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from cart.cart import Cart
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from ..homeapp.models import Movies


@login_required
def add_to_cart(request):
    result = {}
    if request.is_ajax():
        movie_id = request.POST['movie_id']
        quantity = 1
        movie = Movies.objects.get(id=movie_id)
        cart = Cart(request)
        cart.add(movie, movie.price, quantity)
        result['status'] = 'success'
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result['status'] = 'fail'
        return HttpResponse(json.dumps(result), content_type='application/json')

@login_required
def add_to_cart_tmdb(request):
    result = {}
    if request.is_ajax():
        tmdb_id = request.POST['tmdb_id']
        quantity = 1
        movie = Movies.objects.get(tmdb_id=tmdb_id)
        cart = Cart(request)
        cart.add(movie, movie.price, quantity)
        result['status'] = 'success'
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result['status'] = 'fail'
        return HttpResponse(json.dumps(result), content_type='application/json')


@login_required
def remove_from_cart(request):
    result = {}
    if request.is_ajax():
        movie_id = request.POST['movie_id']
        movie = Movies.objects.get(id=movie_id)
        cart = Cart(request)
        cart.remove(movie)
        result['status'] = 'success'
        return HttpResponse(json.dumps(result), content_type="application/json")
    else:
        result['status'] = 'fail'
        return HttpResponse(json.dumps(result), content_type='application/json')


@login_required
def get_cart(request):
    current_cart = Cart(request)
    myCart = Cart.get_cart_details(current_cart)
    return render(request, 'cart.html', {
        'cart': Cart(request),
        'total_items': myCart['total_items'],
        'total_price': myCart['total_price'],
    })