from rest_framework import serializers
from .models import Allocation


class allocation_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Allocation
        fields = "__all__"
            
    
