from django.db import models
from apps.livestock.models import Cow
from apps.farms.models import Farm, Farmer
# Create your models here.

class MilkProduction(models.Model):
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE, related_name='milk_records')
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='milk_records')
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='milk_records')
    date = models.DateField()
    morning_yield_liters = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    evening_yield_liters = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    total_yield_liters = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.total_yield_liters = (self.morning_yield_liters or 0) + (self.evening_yield_liters or 0)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cow.cow_tag} - {self.date} - {self.total_yield_liters} L"