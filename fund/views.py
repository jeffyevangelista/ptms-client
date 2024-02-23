from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import fund_Serializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Fund
from django.http import JsonResponse
from django.middleware.csrf import get_token
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

#api for crud
class Fund_view(ModelViewSet):
    serializer_class = fund_Serializer

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()
    
@permission_classes([IsAuthenticated])
class FundListView(APIView):

    def get(self, request, *args, **kwargs):
        received_token = request.headers.get('Authorization', '').split(' ')[-1]
        print("Received Token:", received_token)
        if request.user.is_authenticated:
            user_id = request.user.id
            funds = Fund.objects.filter(user=user_id)
            serializer = fund_Serializer(funds, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            print("User is not authenticated.")
            return Response({"error": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)
        
