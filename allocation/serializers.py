from rest_framework import serializers
from .models import Allocation


class allocation_Serializer(serializers.ModelSerializer):
    business_name =  serializers.CharField(source='business_unit.business_unit_name', read_only=True)
    fund_name =  serializers.CharField(source='name.name', read_only=True)
    class Meta:
        model = Allocation
        fields = (
            'id',
            'name',
            'business_unit',
            'amount',
            'business_name',
            'fund_name',
        )
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value
            
    
