from rest_framework import serializers
from apps.farms.models import Farm, Farmer
from apps.accounts.models import User
from django.contrib.auth.models import Group

class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = ["name", "location", "agent", "established_date", "is_active", "created_at", "updated_at", "created_by"]

class FarmerSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    # farm = serializers.PrimaryKeyRelatedField(queryset=Farm.objects.all(), required=True)

    class Meta:
        model = Farmer
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'phone', 'address', 'farm', 'is_active']

    def validate_farm(self, farm):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                farms = Farm.objects.get(id=farm.id, created_by=request.user)
                print('farms : ', farms)  
            except Farm.DoesNotExist:
                raise serializers.ValidationError({"Farm": "This Farm does not belong to you."})

        return farm

    def create(self, validated_data):
        first_name = validated_data["first_name"]
        last_name = validated_data["last_name"]
        username = validated_data["username"]
        email = validated_data["email"]
        password = validated_data["password"]

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password,
            created_by = validated_data['created_by'].id,
            is_staff=True
        )

        group = Group.objects.get(name='Farmer')
        user.groups.add(group)

        farmer = Farmer.objects.create(
            user = user,
            farm = validated_data['farm'],
            phone = validated_data['phone'],
            address = validated_data['address'],
            is_active = validated_data['is_active'],
            created_by = validated_data['created_by']
        )

        return farmer




