from django.contrib import admin
from apps.farms.models import Farm, Farmer
from apps.accounts.models import User
from django.contrib.auth.models import Group
from apps.farms.forms import FarmerForm

# Register your models here.

class FarmAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "location", "agent", "created_by", "established_date", "is_active", "created_at")
    list_filter = ("is_active", "established_date", "created_at", "agent")
    search_fields = ("name", "location", "agent__username", "created_by__username")
    readonly_fields = ("created_at", "updated_at")

    list_editable = ("name", "location", "is_active",)
    ordering = ("-created_at",)

    def get_queryset(self, request):
        data = super().get_queryset(request)

        if request.user.is_superuser:
            return data
        
        if request.user.groups.filter(name='SuperAdmin').exists():
            agents = User.objects.filter(created_by=request.user.id)
            return data.filter(created_by=request.user) | data.filter(created_by__in=agents)
        
        if request.user.groups.filter(name='Farmer').exists():
            farmer = Farmer.objects.filter(user=request.user).first()
            if farmer and farmer.farm:
                return data.filter(id=farmer.farm.id)
            return data.none()
        
        return data.filter(agent=request.user)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "agent":
            if request.user.groups.filter(name='SuperAdmin').exists():
                kwargs["queryset"] = User.objects.filter(groups__name='Agent', created_by=request.user.id)

            elif request.user.groups.filter(name='Agent').exists():
                kwargs["queryset"] = User.objects.filter(id=request.user.id) 
                kwargs["initial"] = request.user.id

        if db_field.name == "created_by": 
            kwargs["queryset"] = User.objects.filter(id=request.user.id) 
            kwargs["initial"] = request.user.id

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Farm, FarmAdmin)


class FarmerAdmin(admin.ModelAdmin):
    form = FarmerForm
    list_display = ("id", "user", "farm", "phone", "address", "is_active", "created_by", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")
    list_editable = ("phone", "address", "is_active")
    search_fields = ("user__username", "farm__name", "phone", "address")
    ordering = ("-created_at",)
    
    exclude = ("user",)

    def get_queryset(self, request):
        data = super().get_queryset(request)
        if request.user.is_superuser:
            return data
        elif request.user.groups.filter(name='SuperAdmin').exists():
            agents = User.objects.filter(created_by=request.user.id)
            return data.filter(created_by=request.user) | data.filter(created_by__in=agents)
        elif request.user.groups.filter(name='Agent').exists():
            # agents = User.objects.filter(created_by=request.user.id)
            return data.filter(created_by=request.user) 
        return data.filter(created_by=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "farm":
            if request.user.groups.filter(name='SuperAdmin').exists():
                agents = User.objects.filter(created_by=request.user.id)
                kwargs["queryset"] = Farm.objects.filter(agent__in=agents)

            elif request.user.groups.filter(name='Agent').exists():
                kwargs["queryset"] = Farm.objects.filter(agent=request.user) 

            kwargs["required"] = True

        if db_field.name == "created_by": 
            kwargs["queryset"] = User.objects.filter(id=request.user.id) 
            kwargs["initial"] = request.user.id

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if not change:  
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
                created_by=request.user.id,
                is_staff=True
            )

            group = Group.objects.get(name="Farmer")
            user.groups.add(group)

            obj.user = user
            obj.created_by = request.user

        super().save_model(request, obj, form, change)
    


admin.site.register(Farmer, FarmerAdmin)
