import datetime
from django import template
from django.utils.dateformat import format

register = template.Library()

@register.filter
def custom_date(date):
    return format(date, 'Y')