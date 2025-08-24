from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from apps.livestock.serializers import CowSerializer, CowActivitySerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from system.permissions import IsModelPermissionFactory
from apps.livestock.models import Cow, CowActivity
from apps.farms.models import Farm, Farmer
from apps.accounts.models import User
# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsModelPermissionFactory(Cow)])
def create_cow(request):
    serializer = CowSerializer(data=request.data)
    if serializer.is_valid():
        cow = serializer.save()  
        return Response({
            'msg': 'Cow Created Successfully',
            'cow': CowSerializer(cow).data 
        }, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsModelPermissionFactory(Cow)])
def cow_list(request):
    cows = Cow.objects.none() 

    if request.user.groups.filter(name='SuperAdmin').exists():
        agents = User.objects.filter(created_by=request.user.id)
        farmers = Farmer.objects.filter(created_by__in=agents)
        cows = Cow.objects.filter(farmer__in=farmers)

    elif request.user.groups.filter(name='Agent').exists():
        farmers = Farmer.objects.filter(created_by=request.user.id)
        cows = Cow.objects.filter(farmer__in=farmers)

    elif request.user.groups.filter(name='Farmer').exists():
        farmer = Farmer.objects.filter(user=request.user).first()
        if farmer:
            cows = Cow.objects.filter(farmer=farmer)

    data = []
    for cow in cows:
        data.append({
            "cow_tag": cow.cow_tag,
            "breed": cow.breed,
            "dob": cow.birth_date,
            "farm_name": cow.farmer.farm.name if cow.farmer and cow.farmer.farm else None,
            "farmer": cow.farmer.user.username if cow.farmer and cow.farmer.user else None,
            "gender": cow.gender,
            "weight": cow.weight_kg,
            "is_sold": cow.is_sold,
        })
    
    return Response(data)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsModelPermissionFactory(CowActivity)])
def create_cow_activity(request):
    serializer = CowActivitySerializer(data=request.data, context={'request': request})
    if serializer.is_valid(): 
        cow_activity = serializer.save()
        return Response({
            'msg': 'Activity Created Successfully',
            'activity': CowActivitySerializer(cow_activity).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

     
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsModelPermissionFactory(CowActivity)])
def cow_activity_list(request):
    activities = CowActivity.objects.none()

    if request.user.groups.filter(name='SuperAdmin').exists():
        agents = User.objects.filter(created_by=request.user.id)
        farmers = Farmer.objects.filter(created_by__in=agents)
        activities = CowActivity.objects.filter(recorded_by__in=farmers)

    elif request.user.groups.filter(name='Agent').exists():
        farmers = Farmer.objects.filter(created_by=request.user.id)
        activities = CowActivity.objects.filter(recorded_by__in=farmers)

    elif request.user.groups.filter(name='Farmer').exists():
        farmer = Farmer.objects.filter(user=request.user).first()
        if farmer:
            activities = CowActivity.objects.filter(recorded_by=farmer)

    data = []
    for act in activities:
        data.append({
            "id": act.id,
            "cow_tag": act.cow.cow_tag if act.cow else None,
            "farm_name": act.cow.farmer.farm.name if act.cow and act.cow.farmer and act.cow.farmer.farm else None,
            "farmer": act.recorded_by.user.username if act.recorded_by and act.recorded_by.user else None,
            
            "activity_type": act.activity_type,
            "title": act.title,
            "description": act.description,
            "date": act.date,
            "priority": act.priority,
            "cost": str(act.cost) if act.cost else None,
            "veterinarian": act.veterinarian,
            "medication_used": act.medication_used,
            "next_due_date": act.next_due_date,
            "notes": act.notes,
            "is_completed": act.is_completed,

            "created_at": act.created_at,
            "updated_at": act.updated_at,
        })

    return Response(data)


