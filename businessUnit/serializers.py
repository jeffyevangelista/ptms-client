from rest_framework import serializers
from .models import BusinessUnit

class businessUnit_Serializer(serializers.ModelSerializer):
    fund_name =  serializers.CharField(source='fund.name', read_only=True)
    class Meta:
        model = BusinessUnit
        fields = (
            'id',
            'business_unit_name',
            'fund_name',
            
        )
            
