from django.contrib import admin
from django.urls import path, include

from apps.accounts.views import *

urlpatterns = [
    path("registration/", Registration, name="registration"),
    path('', include('apps.farms.urls')),
    path('', include('apps.livestock.urls')),
    path('', include('apps.production.urls')),
]
