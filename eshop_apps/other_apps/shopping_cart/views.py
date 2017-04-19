# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from cart.cart import Cart
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from ..homeapp.models import Movies
from ..shopping_cart.models import Reservations
import sys

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

@login_required
def checkout(request):
    current_cart = Cart(request)
    myList = ",".join([str(item.product.id) for item in current_cart])
    new_reservation = Reservations(
        delivery_time='2017-04-20 20:00:00',
        user_id=request.user.id,
        session_user_id=request.session.session_key,
        shopping_cart=myList,
        invoice_number=123456,
    )
    new_reservation.save()
    return HttpResponse("Reservation Completed")