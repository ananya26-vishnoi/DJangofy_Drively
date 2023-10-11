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
import string
import random

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
    user = User(name=name, email=email, password=password, role="user")
    user.save()

    # Serialize the user data
    user_serializer = UserSerializer(user)

    # Return a success response
    return Response({"user": user_serializer.data}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login_user(request):
    if "token_value" not in request.data:
        token_value=request.data["token_value"]
        if Token.objects.filter(token_value=token_value).exists():
            token=Token.objects.get(token_value=token_value)
            user_id=token.user_id.id
            user=User.objects.get(id=user_id)
            user_serializer=UserSerializer(user)
            token_serializer=TokenSerializer(token)
            return Response({"user":user_serializer.data,"token":token_serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({"error":"token does not exist"},status=status.HTTP_400_BAD_REQUEST)
    if "email" not in request.data or "password" not in request.data:
        return Response({"error": "email and password are required"}, status=status.HTTP_400_BAD_REQUEST)
    email = request.data["email"]
    password = request.data["password"]

    if not User.objects.filter(email=email, password=password).exists():
        return Response({"error": "email and password wrong"}, status=status.HTTP_400_BAD_REQUEST)
    user=User.objects.get(email=email)
    token_value = ''.join(random.choices(string.ascii_uppercase +string.digits, k=15))
    token=Token.objects.create(user_id=user,token_value=token_value)
    token.save()
    user_serializer=UserSerializer(user)
    token_serializer=TokenSerializer(token)
    return Response({"user":user_serializer.data,"token":token_serializer.data},status=status.HTTP_200_OK)
 

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

    if "new_password" in request.data:
        new_password=request.data["new_password"]
        User.objects.filter(email=email).update(password=new_password)

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
    User.objects.filter(email=email).delete()
    return Response({"success": "user deleted"}, status=status.HTTP_200_OK)

        
@api_view(['GET'])
def file_upload(request):
    if "myfile" not in request.FILES:
        return Response({"error": "file is required"}, status=status.HTTP_400_BAD_REQUEST)
    if "email" not in request.data:
        return Response({"error": "email is required"}, status=status.HTTP_400_BAD_REQUEST)
    email=request.data["email"]
    file_=request.FILES["myfile"]
    if not User.objects.filter(email=email).exists():
        return Response({"error": "email id wrong"}, status=status.HTTP_400_BAD_REQUEST)
    if File.objects.filter(file_name=file_).exists():
        File.objects.filter(file_name=file_).update(file_name=file_)
        file_serializer=FileSerializer(file_)
        return Response({"success": "file updated"}, status=status.HTTP_200_OK)
    
    user=User.objects.get(email=email)
    file=File(file_name=file_,user=user)
    file.save()
    file_serializer=FileSerializer(file)
    return Response(file_serializer.data,status=status.HTTP_200_OK)

@api_view(['DELETE'])
def file_delete(request):
    if "email" not in request.data:
        return Response({"error": "email is required"}, status=status.HTTP_400_BAD_REQUEST)
    if "myfile" not in request.FILES:
        return Response({"error": "file is required"}, status=status.HTTP_400_BAD_REQUEST)
    email = request.data["email"]
    file_ = request.data["myfile"]

    if not User.objects.filter(email=email).exists():
        return Response({"error":"profile does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    user=User.objects.get(email=email)
    file=File(file_name=file_,user=user)
    File.objects.filter(file_name=file_).delete()
    file.save()
    file_serializer=FileSerializer(file)
    return Response({"success": "file deleted"}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_all_files(request):
    if "email" not in request.data:
        return Response({"error": "email is required"}, status=status.HTTP_400_BAD_REQUEST)
    email=request.data["email"]
    if not User.objects.filter(email=email).exists():
        return Response({"error": "email id wrong"}, status=status.HTTP_400_BAD_REQUEST)
    
    
    file_serializer=FileSerializer(file,many=True)
    return Response(file_serializer.data,status=status.HTTP_200_OK)

   