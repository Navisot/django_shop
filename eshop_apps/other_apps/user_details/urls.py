from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^history$', views.get_user_history, name='user_history'),
    url(r'^profile/save$', views.save_personal_details, name='save_personal_details'),
    url(r'^profile$', views.get_user_profile, name='user_profile'),
    url(r'^invoice_pdf$', views.some_view, name='invoice_pdf'),
]