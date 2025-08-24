from django import forms
from django.contrib import admin
from apps.accounts.models import User
from apps.farms.models import Farmer
from django.contrib.auth.models import Group

class FarmerForm(forms.ModelForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    username = forms.CharField()
    email = forms.EmailField(required=False)
    password = forms.CharField()

    class Meta:
        model = Farmer
        fields = "__all__"