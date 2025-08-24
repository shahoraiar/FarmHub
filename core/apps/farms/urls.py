from django.urls import path
from apps.farms.views import *

urlpatterns = [
    path('farm/create/', create_farm, name='create_farm'),
    path('farm/list/', list_farm, name='list_farm'),

    path('farmer/create/', create_farmer, name='create_farmer'),
    path('farmer/list/', list_farmer, name='list_farmer'),
]