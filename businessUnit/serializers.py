from rest_framework import serializers
from .models import BusinessUnit, UserCompanyRelationship


class businessUnit_Serializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessUnit
        fields = "__all__"
            
    
class userCompanyRelationship_Serializer(serializers.ModelSerializer):
    class Meta:
        model = UserCompanyRelationship
        fields = "__all__"