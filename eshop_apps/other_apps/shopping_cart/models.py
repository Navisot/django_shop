# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(default=datetime.now, blank=True)
    delivery_time = models.TimeField(blank=True, null=True)
    delivery_date = models.DateField(blank=True, null=True)
    session_user_id = models.TextField(blank=True)
    shopping_cart = models.TextField(blank=True, null=True)

    def __str__(self):
        return "User: %s - Created: %s" % (self.user_id, self.created)


class Invoices(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(default=datetime.now, blank=True)
    order = models.ForeignKey(Orders, null=True, on_delete=models.CASCADE)
    invoice_identifier = models.IntegerField(null=True)
    session_user_id = models.TextField(blank=True)
    shopping_cart = models.TextField(blank=True, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    telephone = models.CharField(max_length=255, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "First Name: %s - Last Name: %s - Created: %s" % (self.first_name, self.last_name, self.created)