from django.urls import path
from apps.production.views import *

urlpatterns = [
    path('production/cow/milk/', create_milk_record, name='create_milk_record'),
    path('production/cow/milk/list/', milk_production_list, name='milk_production_list'),
  
] 