# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-21 11:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping_cart', '0008_invoices_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoices',
            name='invoice_identifier',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
