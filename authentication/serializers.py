from django.db import models
from django.db.models import fields
from django.db.models.base import Model
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['firstname', 'lastname', 'email', 'password', 'role']

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=68, min_length=7)
    class Meta:
        fields = ["email", "password"]