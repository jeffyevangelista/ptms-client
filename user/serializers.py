from rest_framework import serializers
from .models import User
from django.db import transaction

class user_Serializer(serializers.ModelSerializer):
    business_name = serializers.SerializerMethodField('get_business_unit_names')
    def get_business_unit_names(self, instance):
        business_unit = instance.business_unit.all()
        business_unit_names = [bu.business_unit_name for bu in business_unit]
        return business_unit_names
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
        business_units_data = validated_data.pop('business_unit', [])  # Extracting business units data
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        user.business_unit.set(business_units_data)  # Adding business units to the user
        return user
    
    @transaction.atomic
    def update(self, instance, validated_data):
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
            instance.save()
           
        if 'password' not in validated_data:
            validated_data['password'] = instance.password

        instance = super().update(instance, validated_data)
        return instance
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
