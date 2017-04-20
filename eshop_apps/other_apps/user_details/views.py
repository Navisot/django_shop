# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from ..shopping_cart.models import Reservations

@login_required
def get_user_history(request):
    user_id = request.user.id
    orders = Reservations.objects.get(user_id=user_id)
    return render(request,'user_history.html',{
        'orders': orders
    })
