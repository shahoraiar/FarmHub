from django.db import models
from apps.farms.models import Farm, Farmer
from django.core.exceptions import ValidationError

# Create your models here.
class Cow(models.Model):
    BREED_CHOICES = [
        ('LOCAL', 'Local Breed'),
        ('HOLSTEIN', 'Holstein'),
        ('JERSEY', 'Jersey'),
        ('ANGUS', 'Angus'),
        ('BRAHMAN', 'Brahman'),
        ('CROSSBRED', 'Crossbred'),
        ('OTHER', 'Other'),
    ]
    cow_tag = models.CharField(max_length=50, unique=True)
    breed = models.CharField(max_length=20, choices=BREED_CHOICES, default='LOCAL')
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male','Male'), ('Female', 'Female')], default='Female')
    description = models.CharField(max_length=300, blank=True, null=True)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='cows')
    farmer = models.ForeignKey(Farmer, on_delete=models.SET_NULL, null=True, blank=True, related_name='cows')
    name = models.CharField(max_length=100, blank=True)
    weight_kg = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    color = models.CharField(max_length=50, blank=True)
    mother_tag = models.CharField(max_length=50, blank=True, help_text="Mother's tag ID if known")
    source = models.CharField(max_length=10, choices=[('born', 'Born on farm'),('purchased', 'Purchased'),], default='born', 
                              help_text="Indicates if the cow was born on the farm or purchased")
    purchase_date = models.DateField(null=True, blank=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)

    is_sold = models.BooleanField(default=False)
    sold_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sold_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.cow_tag
    
class CowActivity(models.Model):
    ACTIVITY_TYPES = [
        ('VACCINATION', 'Vaccination'),
        ('HEALTH_CHECK', 'Health Check'),
        ('BREEDING', 'Breeding'),
        ('BIRTH', 'Birth'),
        ('TREATMENT', 'Medical Treatment'),
        ('HOOF_CARE', 'Hoof Care'),
        ('WEIGHT_CHECK', 'Weight Check'),
        ('OTHER', 'Other'),
    ]
    
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('URGENT', 'Urgent'),
    ]
     
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    title = models.CharField(max_length=200, blank=True)
    description = models.CharField(max_length=300, blank=True)
    date = models.DateTimeField(blank=True, null=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    veterinarian = models.CharField(max_length=100, blank=True)
    medication_used = models.CharField(max_length=200, blank=True)
    next_due_date = models.DateField(null=True, blank=True, help_text="When this activity should be repeated")
    recorded_by = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    notes = models.CharField(max_length=300, blank=True)
    is_completed = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

   
