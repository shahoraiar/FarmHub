from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from system.permissions import IsSuperAdminOrAgent, IsModelPermissionFactory
from apps.farms.serializers import FarmSerializer, FarmerSerializer
from rest_framework.response import Response
from rest_framework import status
from apps.farms.models import Farm, Farmer
from apps.accounts.models import User
# Create your views here.

@api_view(['POST']) 
@permission_classes([IsAuthenticated, IsModelPermissionFactory(Farm)]) 
def create_farm(request):
    serializer = FarmSerializer(data=request.data)
    if serializer.is_valid():
        created_by = request.user
        serializer.save(created_by=created_by)
  
        return Response({
            'msg': 'Farm Created Successfully',
            'farm': serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsModelPermissionFactory(Farm)]) 
def list_farm(request):
    if request.user.groups.filter(name='SuperAdmin').exists():
        agents = User.objects.filter(created_by=request.user.id)
        farms = Farm.objects.filter(created_by__in=agents)
    elif request.user.groups.filter(name='Agent').exists():    
        farms = Farm.objects.filter(created_by=request.user)
    else:
        farms = Farm.objects.filter(created_by=request.user)
    serializer = FarmSerializer(farms, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsModelPermissionFactory(Farmer)]) 
def create_farmer(reqeust):
    print('view user : ', reqeust.user)
    serializer = FarmerSerializer(data=reqeust.data, context={'request': reqeust})
    if serializer.is_valid():
        farmer = serializer.save(created_by=reqeust.user)
        return Response({
            "msg": "Farmer created successfully",
            "farmer_id": farmer.id, 
            "username": farmer.user.username,
            "farm": farmer.farm.name if farmer.farm else None
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsModelPermissionFactory(Farmer)]) 
def list_farmer(request):
    if request.user.groups.filter(name='SuperAdmin').exists():
        agents = User.objects.filter(created_by=request.user.id)
        farmers = Farmer.objects.filter(created_by__in=agents)
    elif request.user.groups.filter(name='Agent').exists():
        farmers = Farmer.objects.filter(created_by=request.user.id)
    data = []
    for farmer in farmers:
        data.append({
            "first_name": farmer.user.first_name,
            "last_name": farmer.user.last_name,
            "username": farmer.user.username,
            "email": farmer.user.email,
            "farm_name": farmer.farm.name if farmer.farm else None,
            "phone": farmer.phone,
            "address": farmer.address,
            "is_active": farmer.is_active
        })
    return Response(data) 

    
