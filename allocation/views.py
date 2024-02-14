from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import allocation_Serializer


#api for crud
class Allocation_view(ModelViewSet):
    serializer_class = allocation_Serializer

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()