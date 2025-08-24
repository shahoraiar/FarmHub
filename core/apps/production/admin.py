from django.contrib import admin
from apps.production.models import MilkProduction
from apps.livestock.models import Cow
from apps.farms.models import Farm, Farmer
from apps.accounts.models import User

# Register your models here.

class MilkProductionAdmin(admin.ModelAdmin):
    list_display = ('cow_tag', 'farmer_username', 'farm_name', 'date', 'morning_yield_liters', 'evening_yield_liters', 'total_yield_liters', 'created_at')
    list_filter = ('date', 'farm', 'farmer')
    search_fields = ('cow__cow_tag', 'farmer__user__username', 'farm__name')
    ordering = ('-created_at',)

    list_editable = ('morning_yield_liters', 'evening_yield_liters')
    exclude = ('total_yield_liters', )

    def cow_tag(self, obj):
        return obj.cow.cow_tag if obj.cow.cow_tag else "-"
    cow_tag.short_description = 'Cow Tag'

    def farmer_username(self, obj):
        return obj.farmer.user.username
    farmer_username.short_description = 'Farmer'

    def farm_name(self, obj):
        return obj.farm.name
    farm_name.short_description = 'Farm'

    def save_model(self, request, obj, form, change):
        obj.total_yield_liters = (obj.morning_yield_liters or 0) + (obj.evening_yield_liters or 0)
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        data = super().get_queryset(request)
        if request.user.is_superuser:
            return data
        
        elif request.user.groups.filter(name='SuperAdmin').exists():
            agents = User.objects.filter(created_by=request.user.id)
            farmers = Farmer.objects.filter(created_by__in=agents) 
            cows_milk = MilkProduction.objects.filter(farmer__in=farmers)
            return cows_milk 
        
        elif request.user.groups.filter(name='Agent').exists():
            farmers = Farmer.objects.filter(created_by=request.user) 
            cows_milk = MilkProduction.objects.filter(farmer__in=farmers)
            return cows_milk 
        
        elif request.user.groups.filter(name='Farmer').exists():
            farmer = Farmer.objects.get(user=request.user)
            cows_milk = MilkProduction.objects.filter(farmer=farmer)
            return cows_milk 
        else:
            return MilkProduction.objects.none()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "cow":
            if request.user.groups.filter(name='SuperAdmin').exists():
                agents = User.objects.filter(created_by=request.user.id)
                farmers = Farmer.objects.filter(created_by__in=agents) 
                if farmers:
                    kwargs["queryset"] = Cow.objects.filter(farmer__in=farmers)
                else:
                    kwargs["queryset"] = Cow.objects.none()

            if request.user.groups.filter(name='Farmer').exists():
                farmer = Farmer.objects.get(user=request.user)
                if farmer and farmer.farm:
                    kwargs["queryset"] = Cow.objects.filter(farmer=farmer)
                else:
                    kwargs["queryset"] = Cow.objects.none()

        if db_field.name == "farmer": 
            if request.user.groups.filter(name='SuperAdmin').exists():
                agents = User.objects.filter(created_by=request.user.id)
                farmers = Farmer.objects.filter(created_by__in=agents)
                print('farmer : ', farmers)
                if farmers:
                    kwargs["queryset"] = farmers  
                else:
                    kwargs["queryset"] = Farmer.objects.none()

            if request.user.groups.filter(name='Farmer').exists():
                if request.user.groups.filter(name='Farmer').exists():
                    farmer = Farmer.objects.filter(user=request.user).first()
                    if farmer:
                        kwargs["queryset"] = Farmer.objects.filter(user=request.user)
                        kwargs["initial"] = farmer
                    else:
                        kwargs["queryset"] = Farmer.objects.none()
                        kwargs["initial"] = None

        if db_field.name == "farm":
            if request.user.groups.filter(name='SuperAdmin').exists():
                agents = User.objects.filter(created_by=request.user.id)
                if agents:
                    kwargs["queryset"] = Farm.objects.filter(created_by__in=agents) 
                else:
                    kwargs["queryset"] = Farm.objects.none()

            if request.user.groups.filter(name='Farmer').exists():
                farmer = Farmer.objects.filter(user=request.user).first()
                if farmer and farmer.farm:
                    kwargs["queryset"] = Farm.objects.filter(id=farmer.farm.id)
                    kwargs["initial"] = farmer.farm
                else:
                    kwargs["queryset"] = Farm.objects.none()

        kwargs["required"] = True
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(MilkProduction, MilkProductionAdmin)

