from rest_framework import serializers
from inventory.models import *

class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = '__all__'

class InventoryChangeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryChangeRequest
        fields = '__all__'