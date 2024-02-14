from rest_framework import serializers
from .models import Fund


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
            
    
