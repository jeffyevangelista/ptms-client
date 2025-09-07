from rest_framework import serializers
from .models import User
from django.db import transaction
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class user_Serializer(serializers.ModelSerializer):
    business_name = serializers.SerializerMethodField('get_business_unit_names')
    roles = serializers.SerializerMethodField('get_roles')
    
    def get_business_unit_names(self, instance):
        business_unit = instance.business_unit.all()
        business_unit_names = [bu.business_unit_name for bu in business_unit]
        return business_unit_names
    
    def get_roles(self, instance):
        return [instance.role] if instance.role else []
    
    password = serializers.CharField(write_only=True, min_length=8,required=False)
    
    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'roles',
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

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)  # includes: token_type, exp, jti, user_id

        # Build a single root "user" object for your custom claims
        try:
            bu_qs = user.business_unit.all()
            bu_ids   = list(bu_qs.values_list("id", flat=True))
            bu_names = list(bu_qs.values_list("business_unit_name", flat=True))
            bu_obj = {"ids": bu_ids, "names": bu_names} if bu_ids else None
        except Exception:
            bu_obj = None

        role = getattr(user, "role", None)

        token["user"] = {
            "id": str(user.pk),
            "email": user.email or "",
            "first_name": user.first_name or "",
            "last_name": user.last_name or "",
            "roles": [role] if role else [],
            "business_unit": bu_obj,
        }

        # If you previously added flat claims, drop them to avoid duplication
        for k in ("email", "first_name", "last_name", "roles", "bu_ids", "bu_names"):
            try:
                del token[k]
            except KeyError:
                pass
        return token

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
