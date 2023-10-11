from rest_framework import serializers 
from .models import User,File,Token

class UserSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = User 
        fields = '__all__'

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = '__all__' 

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'