from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('create_inventory_item/', create_inventory_item, name='create_inventory_item'),
    path('', inventory_list, name='inventory_list'),
    path('update_inventory_item/<int:item_id>/', update_inventory_item, name='update_inventory_item'),
    path('delete_inventory_item/<int:item_id>/', delete_inventory_item, name='delete_inventory_item'),
    path('update_status/<int:item_id>/', update_status, name='update_status'),
    
]
