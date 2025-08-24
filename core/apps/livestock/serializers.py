from rest_framework import serializers
from apps.livestock.models import Cow, CowActivity
from apps.farms.models import Farm, Farmer

class CowSerializer(serializers.ModelSerializer):
    farmer = serializers.PrimaryKeyRelatedField(queryset=Farmer.objects.all(), required=True)
    farm = serializers.PrimaryKeyRelatedField(queryset=Farm.objects.all(), required=True)

    class Meta:
        model = Cow
        fields = [
            'cow_tag', 'breed', 'birth_date', 'gender', 'description',
            'farm', 'farmer', 'name', 'weight_kg', 'color', 'mother_tag',
            'source', 'purchase_date', 'purchase_price',
            'is_sold', 'sold_price', 'sold_date'
        ]

    def validate(self, data):
        if data['source'] == 'purchased' and not data.get('purchase_price'):
            raise serializers.ValidationError({"purchase_price": "Purchased cows must have a purchase price."})
        if data['source'] == 'born' and data.get('purchase_price'):
            raise serializers.ValidationError({"purchase_price": "Born cows should not have a purchase price."})

        if data['farmer'].farm != data['farm']:
            raise serializers.ValidationError({"farmer": "This farmer does not belong to the selected farm."})

        return data

    def create(self, validated_data):
        cow = Cow.objects.create(**validated_data)
        return cow
    

class CowActivitySerializer(serializers.ModelSerializer):
    cow = serializers.PrimaryKeyRelatedField(queryset=Cow.objects.all(), required=True)

    class Meta:
        model = CowActivity
        fields = [
            'id', 'cow', 'activity_type', 'title', 'description', 'date',
            'priority', 'cost', 'veterinarian', 'medication_used',
            'next_due_date', 'notes', 'is_completed',
            'created_at', 'updated_at'
        ]
        read_only_fields = ('created_at', 'updated_at')

    def validate_cost(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("Cost cannot be negative.")
        return value

    def validate_cow(self, value):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                farmer = Farmer.objects.get(user=request.user)
            except Farmer.DoesNotExist:
                raise serializers.ValidationError({"cow": "You are not registered as a farmer."})

            if value.farmer != farmer:
                raise serializers.ValidationError({"cow": "This cow does not belong to you."})

        return value 

    def create(self, validated_data):
            request = self.context.get('request')
            if request and request.user.is_authenticated:
                farmer = Farmer.objects.get(user=request.user)
                validated_data['recorded_by'] = farmer
            return super().create(validated_data)     
      

 
