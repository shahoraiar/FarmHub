from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from apps.production.models import MilkProduction
from apps.production.serializers import MilkProductionSerializer
from rest_framework.permissions import IsAuthenticated
from system.permissions import IsModelPermissionFactory
from rest_framework import status
from rest_framework.response import Response
from apps.farms.models import Farmer
from apps.accounts.models import User

# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsModelPermissionFactory(MilkProduction)])
def create_milk_record(request):
    serializer = MilkProductionSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        milk_record = serializer.save()
        return Response({
            "msg": "Milk record created successfully",
            "data": MilkProductionSerializer(milk_record).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsModelPermissionFactory(MilkProduction)])
def milk_production_list(request):
    records = MilkProduction.objects.none()

    if request.user.groups.filter(name='SuperAdmin').exists():
        agents = User.objects.filter(created_by=request.user.id)
        farmers = Farmer.objects.filter(created_by__in=agents)
        records = MilkProduction.objects.filter(farmer__in=farmers)

    elif request.user.groups.filter(name='Agent').exists():
        farmers = Farmer.objects.filter(created_by=request.user.id)
        records = MilkProduction.objects.filter(farmer__in=farmers)

    elif request.user.groups.filter(name='Farmer').exists():
        farmer = Farmer.objects.filter(user=request.user).first()
        if farmer:
            records = MilkProduction.objects.filter(farmer=farmer)

    data = []
    for rec in records:
        data.append({
            "id": rec.id,
            "cow_tag": rec.cow.cow_tag if rec.cow else None,
            "farm_name": rec.farm.name if rec.farm else None,
            "farmer": rec.farmer.user.username if rec.farmer and rec.farmer.user else None,

            "date": rec.date,
            "morning_yield_liters": str(rec.morning_yield_liters),
            "evening_yield_liters": str(rec.evening_yield_liters),
            "total_yield_liters": str(rec.total_yield_liters),

            "created_at": rec.created_at,
            "updated_at": rec.updated_at,
        })

    return Response(data)

