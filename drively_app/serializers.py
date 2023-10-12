from rest_framework import serializers 
from .models import User,File

class UserSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = User 
        fields = ['id', 'name', 'email', 'token_value', 'is_email_verified']

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'