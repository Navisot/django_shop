# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Orders, Invoices

admin.site.register(Orders)
admin.site.register(Invoices)
