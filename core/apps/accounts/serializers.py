from rest_framework import serializers
from apps.accounts.models import User

class RegistrationSerializer(serializers.ModelSerializer):
    user_role = serializers.CharField(required=True)  

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password", "user_role"]