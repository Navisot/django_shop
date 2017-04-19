from django.conf.urls import url

from . import views
from ..shopping_cart.views import checkout as checkout_view

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^movie/(?P<movie_id>[0-9]+)$', views.movie_details, name="movie_details"),
    url(r'^movie/tmdb/(?P<tmdb_id>[0-9]+)$', views.movie_details_by_tmdb, name="movie_details_by_tmdb"),
    url(r'^movie/only_tmdb/(?P<tmdb_id>[0-9]+)$', views.movie_details_only_from_tmdb, name="movie_details_only_by_tmdb"),
    url(r'^movie/genre/(?P<genre_id>[0-9]+)$', views.get_movies_by_genre, name="movie_by_genre"),
    url(r'^search/multi', views.search_movie_multi, name='multi_search'),
    url(r'^cart/checkout/complete$', checkout_view, name='checkout_view'),
]