from django.urls import path
from apps.livestock.views import *

urlpatterns = [
    path('cow/create/', create_cow, name='create_cow'),
    path('cow/list/', cow_list, name='cow_list'),

    path('cow/activity/create/', create_cow_activity, name='create_cow_activity'),
    path('cow/activity/list/', cow_activity_list, name='cow_activity_list'),
     
] 