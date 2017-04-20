from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^history$', views.get_user_history, name='user_history'),
]