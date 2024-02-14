from rest_framework import serializers
from .models import Allocation


class allocation_Serializer(serializers.ModelSerializer):
    business_name =  serializers.CharField(source='business_unit.business_unit_name', read_only=True)
    class Meta:
        model = Allocation
        fields = (
            'id',
            'business_unit',
            'amount',
            'business_name',
        )
            
    
