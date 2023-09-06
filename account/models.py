from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Role(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.name
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roles = models.ManyToManyField(Role,related_name='user_role',blank=True)