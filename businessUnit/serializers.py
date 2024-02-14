from rest_framework import serializers
from .models import BusinessUnit, UserCompanyRelationship

class businessUnit_Serializer(serializers.ModelSerializer):
    fund_name =  serializers.CharField(source='fund.name', read_only=True)
    class Meta:
        model = BusinessUnit
        fields = (
            'id',
            'business_unit_name',
            'fund',
            'fund_name',
        )
            
    
class userCompanyRelationship_Serializer(serializers.ModelSerializer):
    class Meta:
        model = UserCompanyRelationship
        fields = "__all__"