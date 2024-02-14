from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import fund_Serializer


#api for crud
class Fund_view(ModelViewSet):
    serializer_class = fund_Serializer

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()