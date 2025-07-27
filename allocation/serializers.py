from rest_framework import serializers
from .models import Allocation, AllocationLog


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
            

class allocationLog_Serializer(serializers.ModelSerializer):
    fund_name =  serializers.CharField(source='allocation.name', read_only=True)
    business_name =  serializers.CharField(source='allocation.business_unit', read_only=True)
    amount_allocated =  serializers.CharField(source='allocation.amount', read_only=True)
    class Meta:
        model = AllocationLog
        fields = (
            'id',
            'name',
            'amount',
            'fund_name',
            'allocation',
            'business_unit',
            'business_name',
            'amount_allocated',
            'created_at',
        )
