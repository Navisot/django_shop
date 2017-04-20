from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('other_apps.homeapp.urls')),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^cart/', include('other_apps.shopping_cart.urls')),
    url(r'^user/', include('other_apps.user_details.urls')),
]

