# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from ..shopping_cart.models import Orders
from ..homeapp.models import Movies
from cart.cart import Cart
from reportlab.pdfgen import canvas
from django.http import HttpResponse
import datetime

@login_required
def get_user_history(request):
    current_cart = Cart(request)
    myCart = Cart.get_cart_details(current_cart)
    user_id = request.user.id
    orders = Orders.objects.filter(user_id=user_id)
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

@login_required
def get_user_profile(request):
    current_cart = Cart(request)
    myCart = Cart.get_cart_details(current_cart)
    return render(request, 'user_profile.html', {
        'total_items': myCart['total_items'],
        'total_price': myCart['total_price'],
    })

def save_personal_details(request):
    current_cart = Cart(request)
    myCart = Cart.get_cart_details(current_cart)
    user_id = request.user.id
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    # Basic Validation Rules
    if len(first_name) <= 3:
        return render(request, 'user_profile.html', {
            'error_message': 'Please Fill In Your Personal Details Correctly (Min Of 3 Chars is Required)',
            'total_items': myCart['total_items'],
            'total_price': myCart['total_price'],
        })
    if len(last_name) <= 3:
        return render(request, 'user_profile.html', {
            'error_message': 'Please Fill In Your Personal Details Correctly (Min Of 3 Chars is Required)',
            'total_items': myCart['total_items'],
            'total_price': myCart['total_price'],
        })
    if hasNumbers(first_name):
        return render(request, 'user_profile.html', {
            'error_message': 'Please Fill In Your Personal Details Correctly (Min Of 3 Chars is Required)',
            'total_items': myCart['total_items'],
            'total_price': myCart['total_price'],
        })
    if hasNumbers(last_name):
        return render(request, 'user_profile.html', {
            'error_message': 'Please Fill In Your Personal Details Correctly (Min Of 3 Chars is Required)',
            'total_items': myCart['total_items'],
            'total_price': myCart['total_price'],
        })
    # END
    User.objects.filter(pk=user_id).update(first_name=first_name, last_name=last_name)
    return render(request, 'user_profile.html', {
            'success_message': 'Personal Details Successfully Submitted!',
            'total_items': myCart['total_items'],
            'total_price': myCart['total_price'],
        })

def some_view(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)