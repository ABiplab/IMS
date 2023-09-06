from django.urls import path
from .views import *

urlpatterns = [
    path('api_login/', user_login, name='api_login'),
    path('add_inventory/', add_inventory, name='add_inventory'),
    path('fetch_inventory/', fetch_inventory, name='fetch_inventory'),
    path('approve_inventory/', approve_inventory, name='approve_inventory'),
]
