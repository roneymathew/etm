from rest_framework import viewsets, status,filters
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

from .serializers import *
from .models import *

from rest_framework.decorators import api_view,permission_classes,renderer_classes
from rest_framework import permissions
from rest_framework.renderers import BaseRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import uuid
import datetime
import os
User = get_user_model()


from rest_framework.parsers import MultiPartParser
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_admin(request):
    if request.method == 'POST':
        if request.user.user_type == 'AD' or request.user.is_superuser:
            if request.data.get('username',None):
                if request.data.get('password',None) and request.data.get('password1') and request.data.get('password') == request.data.get('password1'):
                    if not User.objects.filter(username = request.data['username']).exists():
                        user = User( user_type = 'AD',username = request.data['username'])
                        user.set_password(request.data['password'])
                        if request.data.get('first_name',None):
                            user.first_name = request.data['first_name']
                        if request.data.get('last_name',None):
                            user.last_name = request.data['last_name']
                        if request.data.get('email',None):
                            user.email = request.data['email']
                        user.save()
                    else:
                        return Response('Username already exists',status = status.HTTP_400_BAD_REQUEST)
                else:
                    return Response("Check your password" , status = status.HTTP_400_BAD_REQUEST)
            else:
                return Response("Provide a username" , status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Permission denied" , status = status.HTTP_400_BAD_REQUEST)
    return Response("all set",status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_empl(request):
    if request.method == 'POST':
        if request.user.user_type == 'AD' or request.user.is_superuser:
            if request.data.get('username',None):
                if request.data.get('password',None) and request.data.get('password1') and request.data.get('password') == request.data.get('password1'):
                    if not User.objects.filter(username = request.data['username']).exists():
                        user = User( user_type = 'EM',username = request.data['username'])
                        user.set_password(request.data['password'])
                        if request.data.get('first_name',None):
                            user.first_name = request.data['first_name']
                        if request.data.get('last_name',None):
                            user.last_name = request.data['last_name']
                        if request.data.get('email',None):
                            user.email = request.data['email']
                        user.save()
                    else:
                        return Response('Username already exists',status = status.HTTP_400_BAD_REQUEST)
                else:
                    return Response("Check your password" , status = status.HTTP_400_BAD_REQUEST)
            else:
                return Response("Provide a username" , status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Permission denied" , status = status.HTTP_400_BAD_REQUEST)
    return Response("all set",status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_manager(request):
    if request.method == 'POST':
        if request.user.user_type == 'AD' or request.user.is_superuser:
            if request.data.get('username',None):
                if request.data.get('password',None) and request.data.get('password1') and request.data.get('password') == request.data.get('password1'):
                    if not User.objects.filter(username = request.data['username']).exists():
                        user = User( user_type = 'MN',username = request.data['username'])
                        user.set_password(request.data['password'])
                        if request.data.get('first_name',None):
                            user.first_name = request.data['first_name']
                        if request.data.get('last_name',None):
                            user.last_name = request.data['last_name']
                        if request.data.get('email',None):
                            user.email = request.data['email']
                        user.save()
                    else:
                        return Response('Username already exists',status = status.HTTP_400_BAD_REQUEST)
                else:
                    return Response("Check your password" , status = status.HTTP_400_BAD_REQUEST)
            else:
                return Response("Provide a username" , status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Permission denied" , status = status.HTTP_400_BAD_REQUEST)
    return Response("all set",status=status.HTTP_200_OK)
