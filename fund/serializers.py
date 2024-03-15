from rest_framework import serializers
from .models import Fund, BusinessUnitInFund ,FundLog

class fund_Serializer(serializers.ModelSerializer):
    first_name =  serializers.CharField(source='user.first_name', read_only=True)
    last_name =  serializers.CharField(source='user.last_name', read_only=True)
    class Meta:
        model = Fund
        fields = (
            'id',
            'name',
            'amount',
            'user',
            'first_name',
            'last_name',

        )

class fundLog_Serializer(serializers.ModelSerializer):
    fund_name =  serializers.CharField(source='fund.name', read_only=True)
    class Meta:
        model = FundLog
        fields = (
            'id',
            'name',
            'amount',
            'user',
            'timestamp',
            'fund',
            'fund_name',

        )


class businessUnitInFund_Serializer(serializers.ModelSerializer):
    name =  serializers.CharField(source='fund_name.name', read_only=True)
    business_name = serializers.SerializerMethodField('get_business_unit_names')
    def get_business_unit_names(self, instance):
        business_units = instance.business_units.all()
        business_unit_names = [bu.business_unit_name for bu in business_units]
        return business_unit_names
    class Meta:
        model = BusinessUnitInFund
        fields = (
            'id',
            'fund_name',
            'business_units',
            'business_name',
            'name',
        ) 
    
