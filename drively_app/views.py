from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import os
from dotenv import load_dotenv 
load_dotenv()
import json
from rest_framework import viewsets
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import Http404
from rest_framework import filters, generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.core.mail import send_mail

#create the user

@api_view(['POST'])
def create_user(request):
    if "name" not in request.data or "email" not in request.data or "password" not in request.data:
        return Response({"error": "name,email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    name=request.data["name"]
    email = request.data["email"]
    password = request.data["password"]
    
    # Check if a user with the same email already exists
    if User.objects.filter(email=email).exists():
        return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

    # Create a new user
    user = User(name=name, email=email, password=password)
    user.save()

    # Serialize the user data
    user_serializer = UserSerializer(user)

    # Return a success response
    return Response({"user": user_serializer.data}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def login_user(request):
    if "email" not in request.data or "password" not in request.data:
        return Response({"error": "email and password are required"}, status=status.HTTP_400_BAD_REQUEST)
    email = request.data["email"]
    password = request.data["password"]

    if not User.objects.filter(email=email, password=password).exists():
        return Response({"error": "email and password wrong"}, status=status.HTTP_400_BAD_REQUEST)
    user=User.objects.get(email=email, password=password)
    user_serializer = UserSerializer(user)
    return Response(user_serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def update_user(request):
    if "email" not in request.data:
        return Response({"error":"email is required"},status=status.HTTP_400_BAD_REQUEST)
    if "password" not in request.data:
        return Response({"error":"password is required"},status=status.HTTP_400_BAD_REQUEST)
    
    email=request.data["email"]
    password=request.data["password"]

    if not User.objects.filter(email=email).exists():
        return Response({"error":"email id wrong"},status=status.HTTP_400_BAD_REQUEST)

    if "password" in request.data:
        password=request.data["password"]
        User.objects.filter(email=email).update(password=password)

    if "name" in request.data:
        name=request.data["name"]
        User.objects.filter(email=email).update(name=name)

    user=User.objects.get(email=email)
    user_serializer=UserSerializer(user)
    return Response(user_serializer.data,status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delete_user(request):
    if "email" not in request.data:
        return Response({"error": "email is required"}, status=status.HTTP_400_BAD_REQUEST)
    if "password" not in request.data:
        return Response({"error": "password is required"}, status=status.HTTP_400_BAD_REQUEST)
    email = request.data["email"]
    password = request.data["password"]

    if not User.objects.filter(email=email, password=password).exists():
        return Response({"error":"profile does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    user=User.objects.get(email=email, password=password)
    User.objects.filter(email=email).delete()
    return Response({"success": "user deleted"}, status=status.HTTP_200_OK)

        
@api_view(['POST'])
def file_upload(request):
    if request.method == 'POST':
        form = File(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse('The file is saved')
    else:
        form = File()
    context = {'form':form,}
    return render(request, 'upload.html', context)
