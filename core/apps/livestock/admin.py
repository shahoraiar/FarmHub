from django.contrib import admin
from apps.livestock.models import Cow, CowActivity
from apps.accounts.models import User
from apps.farms.models import Farm, Farmer
from apps.livestock.models import Cow, CowActivity
# Register your models here.

class CowAdmin(admin.ModelAdmin):
    list_display = ('id', 'cow_tag', 'name', 'breed', 'gender', 'farm', 'farmer', 'weight_kg', 'is_sold', 'created_at') 
    search_fields = ('cow_tag', 'name', 'color', 'mother_tag', 'farmer__user__username', 'farm__name')
    list_filter = ('breed', 'gender', 'source', 'is_sold', 'farm')
    list_editable = ('name', 'weight_kg', 'is_sold')
    ordering = ('-created_at',)

    readonly_fields = ('created_at', 'updated_at')

    def get_queryset(self, request):
        data = super().get_queryset(request)
        if request.user.is_superuser:
            return data
        
        elif request.user.groups.filter(name='SuperAdmin').exists():
            agents = User.objects.filter(created_by=request.user.id)
            farmers = Farmer.objects.filter(created_by__in=agents) 
            cows = Cow.objects.filter(farmer__in=farmers)
            return cows
        
        elif request.user.groups.filter(name='Agent').exists():
            farmers = Farmer.objects.filter(created_by=request.user) 
            cows = Cow.objects.filter(farmer__in=farmers)
            return cows
        
        elif request.user.groups.filter(name='Farmer').exists():
            farmer = Farmer.objects.get(user=request.user)
            cows = Cow.objects.filter(farmer=farmer)
            return cows
        else:
            return Cow.objects.none()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "farm":
            if request.user.groups.filter(name='SuperAdmin').exists():
                agents = User.objects.filter(created_by=request.user.id)
                if agents:
                    kwargs["queryset"] = Farm.objects.filter(created_by__in=agents) 
                else:
                    kwargs["queryset"] = Farm.objects.none()

            elif request.user.groups.filter(name='Farmer').exists():
                farmer = Farmer.objects.filter(user=request.user).first()
                if farmer and farmer.farm:
                    kwargs["queryset"] = Farm.objects.filter(id=farmer.farm.id)
                    kwargs["initial"] = farmer.farm
                else:
                    kwargs["queryset"] = Farm.objects.none()

        if db_field.name == "farmer": 
            if request.user.groups.filter(name='SuperAdmin').exists():
                agents = User.objects.filter(created_by=request.user.id)
                farmers = Farmer.objects.filter(created_by__in=agents)
                print('farmer : ', farmers)
                if farmers:
                    kwargs["queryset"] = farmers  
                else:
                    kwargs["queryset"] = Farmer.objects.none()

            elif request.user.groups.filter(name='Farmer').exists():
                farmer = Farmer.objects.filter(user=request.user).first()
                if farmer:
                    kwargs["queryset"] = Farmer.objects.filter(user=request.user)
                    kwargs["initial"] = farmer
                else:
                    kwargs["queryset"] = Farmer.objects.none()
                    kwargs["initial"] = None

        kwargs["required"] = True
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Cow, CowAdmin)

class CowActivityAdmin(admin.ModelAdmin):
    list_display = ('id', 'cow_tag', 'recorded_by', 'activity_type', 'priority', 'date', 'is_completed', 'cost')
    list_filter = ('activity_type', 'priority', 'is_completed', 'date')
    search_fields = ('cow__cow_tag', 'cow__name', 'recorded_by__user__username', 'title', 'description', 'veterinarian', 'medication_used')
    list_editable = ('is_completed',)
    ordering = ('-date',)
    
    def cow_tag(self, obj):
        return obj.cow.cow_tag
    cow_tag.short_description = 'Cow Tag'

    def get_queryset(self, request):
        data = super().get_queryset(request)
        if request.user.is_superuser:
            return data
        
        elif request.user.groups.filter(name='SuperAdmin').exists():
            agents = User.objects.filter(created_by=request.user.id)
            farmers = Farmer.objects.filter(created_by__in=agents) 
            cows = CowActivity.objects.filter(recorded_by__in=farmers)
            return cows 
        
        elif request.user.groups.filter(name='Agent').exists():
            farmers = Farmer.objects.filter(created_by=request.user.id) 
            cows = CowActivity.objects.filter(recorded_by__in=farmers)
            return cows

        elif request.user.groups.filter(name='Farmer').exists():
            farmer = Farmer.objects.get(user=request.user)
            cows = CowActivity.objects.filter(recorded_by=farmer)
            return cows  
        else:
            return CowActivity.objects.none()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "cow":
            if request.user.groups.filter(name='SuperAdmin').exists():
                agents = User.objects.filter(created_by=request.user.id)
                farmers = Farmer.objects.filter(created_by__in=agents) 
                if farmers:
                    kwargs["queryset"] = Cow.objects.filter(farmer__in=farmers)
                else:
                    kwargs["queryset"] = Cow.objects.none()

            elif request.user.groups.filter(name='Farmer').exists():
                farmer = Farmer.objects.get(user=request.user)
                if farmer and farmer.farm:
                    kwargs["queryset"] = Cow.objects.filter(farmer=farmer)
                else:
                    kwargs["queryset"] = Cow.objects.none()

        if db_field.name == "recorded_by":
            if request.user.groups.filter(name='SuperAdmin').exists():
                agents = User.objects.filter(created_by=request.user.id)
                if agents:
                    kwargs["queryset"] = Farmer.objects.filter(created_by__in=agents)
                else:
                    kwargs["queryset"] = Farmer.objects.none()

            if request.user.groups.filter(name='Farmer').exists():
                farmer = Farmer.objects.filter(user=request.user).first()
                if farmer:
                    kwargs["queryset"] = Farmer.objects.filter(user=request.user)
                    kwargs["initial"] = farmer
                else:
                    kwargs["queryset"] = Farmer.objects.none()
                    kwargs["initial"] = None

        kwargs["required"] = True
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(CowActivity, CowActivityAdmin)


