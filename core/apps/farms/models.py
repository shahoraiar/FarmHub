from django.db import models
from apps.accounts.models import User

# Create your models here.
class Farm(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=300)
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'groups__name__in': ['Agent', 'SuperAdmin']})
    established_date = models.DateField(null=True, blank=True)
    area_hectares = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='create_admin')
    
    def __str__(self):
        return self.name

class Farmer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=300, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="farmer_admin", limit_choices_to={'groups__name__in': ['SuperAdmin', 'Agent']})
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    
    def __str__(self):
        return f"{self.user.username}"
    
