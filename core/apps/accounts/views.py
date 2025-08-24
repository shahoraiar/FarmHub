from django.shortcuts import render, redirect

# Create your views here.
from rest_framework import serializers, status
from rest_framework.response import Response
from django.contrib.auth.models import Group
from apps.accounts.serializers import RegistrationSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from apps.accounts.models import User

def admin_redirect_login(request):
    return redirect("/") 

@api_view(['POST'])
@permission_classes([AllowAny])
def Registration(request):
    print('request : ', request)
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user_role = serializer.validated_data['user_role']

        group = Group.objects.filter(name=user_role).first()
        if not group:
            return Response(
                {"user_role": ["This role does not exist."]},
                status=status.HTTP_400_BAD_REQUEST
            )

        if user_role == 'SuperAdmin' and not request.user.is_authenticated:
            created_by = 0
        
        else:
            if not request.user.is_authenticated:
                return Response({"error": "Authentication required to create this Role User."}, status=403)
            created_by = request.user.id
            print('created by : ', created_by)

            if user_role == 'SuperAdmin' and not request.user.is_superuser:
                return Response({"error": "Only SuperUser can create SuperAdmin."}, status=403)

            if user_role == 'Agent' and not request.user.groups.filter(name='SuperAdmin').exists():
                return Response({"error": "Only SuperAdmin can create Agents."}, status=403)

            if user_role == 'Farmer' :
                return Response({"error": "From Farmers can create Farmer Role User."}, status=403)
         
        user = User.objects.create_user(
            first_name = serializer.validated_data['first_name'],
            last_name = serializer.validated_data['last_name'],
            username =serializer.validated_data['username'],
            email = serializer.validated_data['email'],
            password = serializer.validated_data['password'],
            created_by = created_by,
            is_staff=True
        )
        user.groups.add(group)

        return Response({
            'msg': 'Registration Success'
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)









