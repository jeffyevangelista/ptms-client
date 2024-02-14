from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import businessUnit_Serializer,userCompanyRelationship_Serializer


class BusinessUnit_view(ModelViewSet):
    serializer_class = businessUnit_Serializer

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()
    
class UserCompanyRelationship_view(ModelViewSet):
    serializer_class = userCompanyRelationship_Serializer

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()