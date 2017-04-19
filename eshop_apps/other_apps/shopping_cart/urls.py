from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^add/$', views.add_to_cart, name="add_to_cart"),
    url(r'^add/tmdb/$', views.add_to_cart, name="add_to_cart_tmdb"),
    url(r'^remove/$', views.remove_from_cart, name="remove_from_cart"),
    url(r'^show$', views.get_cart, name="get_cart"),
]