from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.accounts.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group
from django.urls import reverse
from django.http import HttpResponseRedirect

# Register your models here.
class Users(UserAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'get_user_role', 'created_by')
    list_editable = ('first_name', 'last_name', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    list_filter = ('is_active', 'is_staff', 'groups')
    ordering = ('id',)

    def get_user_role(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])
    get_user_role.short_description = "Role" 

    # Fields for adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'groups'),
        }),
    ) 

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not obj: 
            if request.user.is_superuser:
                agent_group = Group.objects.filter(name__in=['SuperAdmin', 'Agent'])
            elif request.user.groups.filter(name='SuperAdmin').exists():
                agent_group = Group.objects.filter(name="Agent")

            form.base_fields['groups'].queryset = agent_group
            form.base_fields['groups'].required = True 
        
        return form

    def get_queryset(self, request):
        data = super().get_queryset(request)
        if request.user.is_superuser:
            return data
        if request.user.groups.filter(name='SuperAdmin').exists():
            agents = User.objects.filter(created_by=request.user.id)
            farmers = User.objects.filter(created_by__in=agents)
            return data.filter(id=request.user.id) | agents | farmers

        return data.filter(created_by=request.user.id) | data.filter(id=request.user.id)

    
    def save_model(self, request, obj, form, change):
        if not obj.pk:  
            obj.created_by = request.user.id
            obj.is_staff = True
        super().save_model(request, obj, form, change)

    def response_add(self, request, obj, post_url_continue=None):
        opts = self.model._meta
        changelist_url = reverse('admin:%s_%s_changelist' % (opts.app_label, opts.model_name))
        return HttpResponseRedirect(changelist_url)


admin.site.register(User, Users)

admin.site.site_header = "FarmHub Administration"
# admin.site.site_title = "FarmHub Admin Portal"
admin.site.index_title = "Welcome to FarmHub Administration"