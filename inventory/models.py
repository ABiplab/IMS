from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class ApprovedInventoryItemManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=InventoryChangeRequest.Status.APPROVED)

class InventoryItem(models.Model):

    product_id = models.CharField(max_length=50)
    product_name = models.CharField(max_length=100)
    vendor = models.CharField(max_length=100)
    mrp = models.DecimalField(max_digits=10, decimal_places=2)
    batch_num = models.CharField(max_length=50)
    batch_date = models.DateField()
    quantity = models.PositiveIntegerField()
    
    class Meta:
        ordering =  ['-product_name']
        indexes = [
            models.Index(fields=['product_name']),
        ]
    def __str__(self) -> str:
        return self.product_name
    
class InventoryChangeRequest(models.Model):
    class RequestType(models.TextChoices):
        ADD = 'AD' , 'Add'
        UPDATE = 'UP' , 'Update'
        DELETE = 'DE' , 'Delete'
    class Status(models.TextChoices):
        APPROVED = 'AP' , 'Approved'
        PENDING = 'PE' , 'Pending'
    inventory_item = models.ForeignKey(InventoryItem, related_name='inventory_item', on_delete=models.CASCADE)
    department_manager = models.ForeignKey(User, related_name='change_requests', on_delete=models.CASCADE, null=True)
    store_manager = models.ForeignKey(User, related_name='approved_requests', on_delete=models.CASCADE, null=True)
    request_type = models.CharField(max_length=2,choices=RequestType.choices) 
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2,choices=Status.choices,default=Status.PENDING)
    objects = models.Manager() 
    approved_objects = ApprovedInventoryItemManager() 