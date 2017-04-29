from django.conf.urls import url

from ..shopping_cart.views import checkout as checkout_view
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^movie/(?P<movie_id>[0-9]+)$', views.movie_details, name="movie_details"),
    url(r'^movie/tmdb/(?P<tmdb_id>[0-9]+)$', views.movie_details_by_tmdb, name="movie_details_by_tmdb"),
    url(r'^movie/tmdb/details/(?P<tmdb_id>[0-9]+)$', views.movie_details_only_from_tmdb, name="movie_details_only_by_tmdb"),
    url(r'^movie/genre/(?P<genre_title>[\w ]+)$', views.get_movies_by_genre, name="movie_by_genre"),
    url(r'^search/multi', views.search_movie_multi, name='multi_search'),
    url(r'^search/actor', views.search_movie_by_actor, name='search_movie_by_actor'),
    url(r'^cart/checkout/complete$', checkout_view, name='checkout_view'),
]