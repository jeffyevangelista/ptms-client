from rest_framework import serializers
from .models import Fund


class fund_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Fund
        fields = "__all__"
            
    
