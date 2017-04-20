# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from ..shopping_cart.models import Reservations
from ..homeapp.models import Movies
from cart.cart import Cart
import datetime

@login_required
def get_user_history(request):
    current_cart = Cart(request)
    myCart = Cart.get_cart_details(current_cart)
    user_id = request.user.id
    orders = Reservations.objects.filter(user_id=user_id)
    full_results = []
    for order in orders:
        temp_movies = order.shopping_cart
        temp = {'order_id': order.id, 'movies': temp_movies.split(","), 'created': order.created}
        full_results.append(temp)
    total = []
    for result in full_results:
        for movie in result['movies']:
            movie_details = Movies.objects.get(pk=movie)
            temp = {'order_id': result['order_id'], 'title': movie_details.title, 'movie_id': movie}
            total.append(temp)
    return render(request, 'user_history.html', {
        'orders': orders,
        'movies': total,
        'total_items': myCart['total_items'],
        'total_price': myCart['total_price'],
    })
