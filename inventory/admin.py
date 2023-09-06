from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'product_name', 'vendor', 'mrp', 'batch_num', 'batch_date', 'quantity')
    # list_filter = ('status',)
    search_fields = ('product_id', 'product_name', 'vendor', 'batch_num')
    ordering = ('-product_name',)
    # list_editable = ('status',)
@admin.register(InventoryChangeRequest)
class InventoryChangeRequestAdmin(admin.ModelAdmin):
    list_display = ('inventory_item', 'department_manager', 'store_manager', 'request_type', 'request_date','status')
    list_filter = ('request_type','status')
    search_fields = ('inventory_item__product_id', 'inventory_item__product_name', 'department_manager__username')
    ordering = ('-request_date',)
    list_editable = ('status','request_type')

