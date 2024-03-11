from rest_framework import serializers
from .models import User
from django.db import transaction

class user_Serializer(serializers.ModelSerializer):
    business_name =  serializers.CharField(source='business_unit.business_unit_name', read_only=True)
    password = serializers.CharField(write_only=True, min_length=8,required=False)
    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'role',
            'business_unit',
            'business_name',
            'password',
            'active',
        )
    
    @transaction.atomic
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    @transaction.atomic
    def update(self, instance, validated_data):
        # Handle password update only if provided
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)

        # Update other fields
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.role = validated_data.get('role', instance.role)
        instance.business_unit = validated_data.get('business_unit', instance.business_unit)
        instance.active = validated_data.get('active', instance.active)

        instance.save()
        return instance
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)