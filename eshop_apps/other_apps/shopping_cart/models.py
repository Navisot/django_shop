# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Reservations(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(default=datetime.now, blank=True)
    delivery_time = models.DateTimeField(blank=True)
    invoice_number = models.IntegerField(blank=True)
    session_user_id = models.TextField(blank=True)
    shopping_cart = models.TextField(blank=True, null=True)

    def __str__(self):
        return "User: %s - Created: %s" % (self.user_id, self.created)