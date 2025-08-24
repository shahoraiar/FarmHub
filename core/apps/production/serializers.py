from apps.production.models import MilkProduction
from rest_framework import serializers
from apps.livestock.models import Cow
from apps.farms.models import Farm, Farmer

class MilkProductionSerializer(serializers.ModelSerializer):
    cow = serializers.PrimaryKeyRelatedField(queryset=Cow.objects.all(), required=True)
 
    class Meta:
        model = MilkProduction
        fields = [
            'cow', 'farmer', 'farm', 'date', 
            'morning_yield_liters', 'evening_yield_liters', 'total_yield_liters',
            'created_at', 'updated_at'
        ]
        read_only_fields = ('farmer', 'farm', 'total_yield_liters', 'created_at', 'updated_at')

    def validate_cow(self, value):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                farmer = Farmer.objects.get(user=request.user)
            except Farmer.DoesNotExist:
                raise serializers.ValidationError({"cow","You are not registered as a farmer."})

            if value.farmer != farmer:
                raise serializers.ValidationError({"cow", "This cow does not belong to you."})
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            farmer = Farmer.objects.get(user=request.user)
            validated_data['farmer'] = farmer
            validated_data['farm'] = validated_data['cow'].farm
        return super().create(validated_data)
