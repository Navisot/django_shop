# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from ..shopping_cart.models import Orders, Invoices
from ..homeapp.models import Movies
from cart.cart import Cart
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from suds.client import Client
from suds.cache import NoCache
from datetime import datetime
import json
import ast


@login_required
def get_user_history(request):
    current_cart = Cart(request)
    myCart = Cart.get_cart_details(current_cart)
    user_id = request.user.id
    orders = Orders.objects.filter(user_id=user_id)
    invoices = Invoices.objects.filter(user_id=user_id)
    full_results = []
    i = 0
    for order in orders:
        temp_movies = order.shopping_cart
        temp = {'order_id': order.id, 'movies': temp_movies.split(","), 'created': order.created}
        full_results.append(temp)
        i += 1
    total = []
    for result in full_results:
        for movie in result['movies']:
            movie_details = Movies.objects.get(pk=movie)
            temp = {'order_id': result['order_id'], 'title': movie_details.title, 'movie_id': movie}
            total.append(temp)
    return render(request, 'user_history.html', {
        'orders': orders,
        'movies': total,
        'invoices': invoices,
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


@login_required
def create_pdf(request, invoice_id):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    # Create the PDF object, using the response object as its "file."
    document = canvas.Canvas(response)
    invoice_details = Invoices.objects.get(pk=invoice_id)
    order_details = Orders.objects.get(pk=invoice_details.order_id)
    movie_details = invoice_details.shopping_cart.split(",")
    movie_titles = []
    for m in movie_details:
        mov = Movies.objects.get(pk=m)
        temp = {'title': mov.title}
        movie_titles.append(temp)
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    document.setStrokeColorRGB(0.13, 0.55, 0.87)
    document.setFillColorRGB(0.2, 0.2, 0.2)
    document.setFont('Helvetica', 16)
    document.drawCentredString(300, 820, "DVDSTORE PURCHASE")
    document.setFont('Helvetica', 14)
    document.drawCentredString(300, 780, 'Invoice #' + str(invoice_details.invoice_identifier))
    document.drawCentredString(300, 750, str(invoice_details.first_name) + ' ' + str(invoice_details.last_name))
    document.drawCentredString(300, 720, str(invoice_details.email))
    document.drawCentredString(300, 690, 'Date: ' + str(invoice_details.created.strftime("%d %B, %Y")))
    if invoice_details.telephone is not None:
        document.drawCentredString(300, 660, str(invoice_details.telephone))
    if invoice_details.company is not None:
        document.drawCentredString(300, 630, str(invoice_details.company))
    document.setFont('Helvetica', 16)
    document.drawCentredString(300, 570, "SELECTED MOVIES:")
    i = 540
    x = 1
    document.setFont('Helvetica', 12)
    for movie in movie_titles:
        document.drawCentredString(300, i, str(x) + '. ' + movie['title'])
        i -= 20
        x += 1
    document.setFont('Helvetica', 14)
    document.drawCentredString(300, i-30, "Total Order Price: €" + str(order_details.total_order_price))
    # Close the PDF object cleanly, and we're done.
    document.showPage()
    document.save()
    return response


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


def test_client(request):
    client = Client('http://soap.dev/server.php?wsdl', cache=NoCache())
    return HttpResponse("Client: " + str(client.service.getQuantity(2)))