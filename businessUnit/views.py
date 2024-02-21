from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import businessUnit_Serializer

class BusinessUnit_view(ModelViewSet):
    serializer_class = businessUnit_Serializer

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()
    
