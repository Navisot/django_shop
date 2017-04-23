# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from cart.cart import Cart
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from ..homeapp.models import Movies
from ..shopping_cart.models import Orders, Invoices
import datetime
import random

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


def get_checkout_review(request):
    current_cart = Cart(request)
    myCart = Cart.get_cart_details(current_cart)
    return render(request, 'checkout_review.html', {
        'cart': Cart(request),
        'total_items': myCart['total_items'],
        'total_price': myCart['total_price'],
    })

@login_required
def checkout(request):
    # Get Current Cart
    current_cart = Cart(request)
    # END
    myCart = Cart.get_cart_details(current_cart)
    logged_in_user = User.objects.get(pk=request.user.id)
    first_name = logged_in_user.first_name
    last_name = logged_in_user.last_name
    email = logged_in_user.email
    error_message = "Please Fill In Your Personal Details (First Name, Last Name) In USER PROFILE section."
    telephone_error = 'Please correct the telephone number.'

    telephone = request.POST.get('telephone')
    company = request.POST.get('company_name')

    if telephone and not telephone.isdigit():
        return render(request, 'checkout_review.html', {
            'error_message': telephone_error,
            'cart': Cart(request),
            'total_items': myCart['total_items'],
            'total_price': myCart['total_price']})

    if not first_name:
        return render(request, 'checkout_review.html', {
            'error_message': error_message,
            'cart': Cart(request),
            'total_items': myCart['total_items'],
            'total_price': myCart['total_price']})
    if not last_name:
        return render(request, 'checkout_review.html', {
            'error_message': error_message,
            'cart': Cart(request),
            'total_items': myCart['total_items'],
            'total_price': myCart['total_price']})
    if not email:
        return render(request, 'checkout_review.html', {
            'error_message': error_message,
            'cart': Cart(request),
            'total_items': myCart['total_items'],
            'total_price': myCart['total_price'],})

    # Get Current Cart
    current_cart = Cart(request)
    # END

    # Check If Cart Is Empty And Return To Homepage
    if myCart['total_items'] == 0:
        context = Movies.objects.all()
        return render(request, 'homepage.html', {
            'data': context,
            'homepage': True,
            'total_items': myCart['total_items'],
            'total_price': myCart['total_price'],
        })
    # END

    # Create List To Store In DB
    myList = ",".join([str(item.product.id) for item in current_cart])
    # END

    all_products = []
    for item in current_cart:
        temp = {'item_id': item.product.id, 'item_title': item.product.title, 'quantity': item.quantity, 'price': str(item.total_price)}
        all_products.append(temp)
    json_products = json.dumps(all_products)

    # Get Post DateTime Details And Create DateTime Objects
    delivery_time = request.POST.get('timepicker')
    delivery_date = request.POST.get('datepicker')
    object_date = datetime.datetime.strptime(delivery_date, '%d-%m-%Y')
    object_time = datetime.datetime.strptime(delivery_time, '%H:%M:%S')
    # END

    # Format Date To Store In DB
    dt_store = object_date.date()
    # END

    # Save Cart Details In Order To Appear Later On Checkout Details
    cart_details_for_template = []
    for item in Cart(request):
        cart_details_for_template.append(item)
    # END

    # Add New Order
    new_order = Orders(
        user_id=request.user.id,
        session_user_id=request.session.session_key,
        shopping_cart=myList,
        shopping_cart_details=json_products,
        delivery_date=dt_store,
        delivery_time=delivery_time,
        total_order_price=myCart['total_price']
    )
    new_order.save()
    # END

    # Get Latest Order Id
    last_order_id = Orders.objects.latest('id')
    #END

    # Generate Random Invoice Number
    random_number = str(random.randint(1000000, 10000000))
    # END

    # Add new Invoice
    new_invoice = Invoices(
        user_id=request.user.id,
        order=last_order_id,
        invoice_identifier=random_number,
        session_user_id=request.session.session_key,
        shopping_cart=myList,
        first_name=first_name,
        last_name=last_name,
        email=email,
        telephone=telephone,
        company=company,
    )
    new_invoice.save()
    # END

    # Clear Current Cart
    current_cart.clear()
    # END

    return render(request, 'order_completed.html', {
        'cart': cart_details_for_template,
        'delivery_time': object_time,
        'delivery_date': object_date,
        'total_items': 0,
        'total_price': 0,
    })